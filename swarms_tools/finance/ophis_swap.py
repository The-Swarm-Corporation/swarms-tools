"""Ophis (CoW Protocol) MEV-protected swap tool for the Swarms framework.

Add this to `swarms_tools/finance/` and export it in that package's `__init__.py`.
A swarms tool is a plain, sync, type-hinted function with a Google-style docstring;
the `swarms` runtime auto-generates the schema from the signature. This one performs
a full same-chain ERC-20 swap through Ophis: it quotes, builds the Ophis partner-fee
appData, approves the CoW VaultRelayer, EIP-712-signs the GPv2 order with the agent's
key, and submits it. Settlement is gasless, MEV-protected, surplus-returning.

The signer key is read from the environment (`OPHIS_PRIVATE_KEY`, or `PRIVATE_KEY` /
`TRANSMITTER_PRIVATE_KEY`), matching the swarms-tools on-chain convention. It is used
locally with eth_account and never logged or transmitted.
"""
from __future__ import annotations

import json
import os
import time

try:
    from . import ophis_core as oc
except ImportError:  # loaded flat rather than as a package
    import ophis_core as oc  # type: ignore[no-redef]

MAX_SLIPPAGE_BPS = 5_000  # 50%
ORDER_TTL_SECONDS = 1_200  # order valid ~20 min; self-set, never the quote's
_KEY_ENV_VARS = ("OPHIS_PRIVATE_KEY", "PRIVATE_KEY", "TRANSMITTER_PRIVATE_KEY")


def _load_account():
    """Load the signer from env. Returns an eth_account LocalAccount (never logs the key)."""
    key = None
    for var in _KEY_ENV_VARS:
        val = os.getenv(var)
        if val and val.strip():
            key = val.strip()
            break
    if not key:
        raise ValueError(
            f"no signer key in env — set one of {', '.join(_KEY_ENV_VARS)} to the agent wallet's private key"
        )
    from eth_account import Account

    return Account.from_key(key if key.startswith("0x") else f"0x{key}")


def _send_signed_tx(account, chain_id: int, to: str, data: str, nonce: int) -> tuple[str, int]:
    """Build a legacy tx, sign locally with eth_account, broadcast. Returns (tx_hash, next_nonce)."""
    gas_price = oc.get_gas_price(chain_id)
    est = {"from": account.address, "to": to, "data": data, "value": "0x0"}
    try:
        gas = int(oc.estimate_gas(chain_id, est) * 12 // 10)  # +20% headroom
    except RuntimeError:
        gas = 120_000  # ERC-20 approve is ~46k; a safe fixed fallback if estimate fails
    tx = {
        "to": to, "value": 0, "data": data, "chainId": int(chain_id),
        "nonce": nonce, "gas": gas, "gasPrice": gas_price,
    }
    signed = account.sign_transaction(tx)
    raw = signed.raw_transaction
    tx_hash = oc.send_raw_transaction(chain_id, "0x" + raw.hex() if not raw.hex().startswith("0x") else raw.hex())
    return tx_hash, nonce + 1


def _wait_receipt(chain_id: int, tx_hash: str, timeout: int = 180) -> None:
    """Block until the tx is mined; raise if it reverted or never mines in time."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        receipt = oc.get_transaction_receipt(chain_id, tx_hash)
        if isinstance(receipt, dict) and receipt.get("blockNumber") is not None:
            status = receipt.get("status")
            # Mined != successful. Require status EXACTLY 1 (accept hex string or int); a missing
            # or non-1 status means the approval did not take, so refuse to sign against it.
            if status is None:
                raise RuntimeError(f"approval tx {tx_hash} receipt has no status; refusing to proceed")
            s = int(status, 16) if isinstance(status, str) else int(status)
            if s != 1:
                raise RuntimeError(f"approval tx {tx_hash} reverted on-chain (status {s})")
            return
        time.sleep(3)
    raise RuntimeError(f"approval tx {tx_hash} not mined within {timeout}s")


def ophis_swap(
    sell_token: str,
    buy_token: str,
    amount: str,
    chain: str = "base",
    slippage_bps: int = 50,
    referral_code: str = "",
) -> str:
    """Swap one ERC-20 for another on the SAME chain via Ophis (CoW Protocol): MEV-protected,
    gasless at settlement, surplus returned. Signs a GPv2 order with the agent's key (from env)
    and submits it to the Ophis orderbook. Native ETH is not supported (wrap to WETH). This is
    a same-chain swap, not a bridge.

    Args:
        sell_token (str): ERC-20 sell token contract address (0x...).
        buy_token (str): ERC-20 buy token contract address (0x...).
        amount (str): Amount of sell_token in WHOLE units, e.g. "100" or "1.5".
        chain (str): Chain name or id — e.g. "base", "ethereum", "arbitrum", "optimism",
            "polygon", "bnb", "gnosis", "avalanche", "unichain", "linea", "ink", or a chain id.
        slippage_bps (int): Max slippage in basis points (0-5000). Default 50 (0.5%).
        referral_code (str): Ophis referral code that earns the rebate. Optional ("" for none).
        (The 1bp stable-pair fee tier is applied automatically when both tokens are in the
        verified stablecoin registry — it is derived, never a caller argument.)

    Returns:
        str: A JSON string. On success: {"ok": true, "order_uid", "explorer_url", ...}. On
            failure: {"ok": false, "error": "..."}. Never raises.
    """
    try:
        chain_id = oc.resolve_chain(chain)
        if not (0 <= slippage_bps <= MAX_SLIPPAGE_BPS):
            raise ValueError(f"slippage_bps must be within [0, {MAX_SLIPPAGE_BPS}] (0%..50%)")

        from eth_utils import to_checksum_address

        sell = to_checksum_address(sell_token)
        buy = to_checksum_address(buy_token)
        zero = "0x0000000000000000000000000000000000000000"
        native = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
        if sell.lower() in (zero, native) or buy.lower() in (zero, native):
            raise ValueError("Ophis EOA orders are ERC-20 only; wrap native to WETH first (native uses CoW eth-flow).")

        account = _load_account()
        owner = account.address

        sell_decimals = oc.read_decimals(chain_id, sell)
        sell_atomic = oc.to_atomic(amount, sell_decimals)
        if sell_atomic > oc.MAX_UINT256:
            raise ValueError(f"sell amount {sell_atomic} exceeds uint256")

        oc.enroll_wallet(owner)  # best-effort rebate enrollment; never raises

        # 1-2. Ophis partner-fee appData + quote (quote carries the appData HASH).
        is_stable_pair = oc.is_stable_pair(chain_id, sell, buy)  # derived, not caller-controlled
        full_app_data, app_hash = oc.build_app_data(referral_code=referral_code or None, is_stable_pair=is_stable_pair)
        quote = oc.get_quote(chain_id, sell, buy, sell_atomic, owner, app_hash)
        if not isinstance(quote, dict):
            raise RuntimeError(f"orderbook quote was not an object: {quote!r}")
        for field in ("sellToken", "buyToken", "sellAmount", "buyAmount", "feeAmount"):
            if field not in quote:
                raise RuntimeError(f"orderbook quote is missing required field {field!r}: {quote}")
        quote_buy = int(quote["buyAmount"])
        quote_sell = int(quote["sellAmount"])
        quote_fee = int(quote["feeAmount"])

        # Bind the SIGNED order to the request — never sign fields drifted from intent. Tokens
        # must echo the request (a compromised/misconfigured orderbook could otherwise quote a
        # different pair and its buyAmount would become a wrong price floor for OUR pair).
        if to_checksum_address(str(quote["sellToken"])) != sell:
            raise RuntimeError(f"quote sellToken {quote['sellToken']} != requested {sell}; refusing")
        if to_checksum_address(str(quote["buyToken"])) != buy:
            raise RuntimeError(f"quote buyToken {quote['buyToken']} != requested {buy}; refusing")
        # We ALWAYS sign feeAmount 0 (Ophis/CoW take the fee from surplus + the appData partner
        # fee), so bind the GROSS (quote sellAmount + feeAmount) to the requested amount rather than
        # rejecting a quote that split a non-zero fee out. An honest sell quote's gross equals the
        # request exactly; any drift (over or under) means a bad/hostile quote.
        gross = quote_sell + quote_fee
        if gross != sell_atomic:
            raise RuntimeError(f"quote gross (sellAmount+feeAmount = {gross}) != requested ({sell_atomic}); refusing to sign")
        if not (0 < quote_buy <= oc.MAX_UINT256):
            raise RuntimeError(f"quote buyAmount out of range (0, uint256]: {quote_buy}")

        min_buy = quote_buy * (10_000 - slippage_bps) // 10_000
        if min_buy <= 0:
            raise RuntimeError("computed minimum buy amount is 0 — refusing an accept-any-price order")

        valid_to = int(time.time()) + ORDER_TTL_SECONDS  # self-set, not the quote's expiry

        # 3. Publish the full appData so solvers honor the partner fee for this hash.
        oc.put_app_data(chain_id, app_hash, full_app_data)

        # 4. Approve the CoW VaultRelayer for EXACTLY the sell amount (allowance-aware, USDT-safe).
        relayer = oc.vault_relayer(chain_id)
        current = oc.read_allowance(chain_id, sell, owner, relayer)
        if current < sell_atomic:
            nonce = oc.get_nonce(chain_id, owner)
            if current > 0:
                # USDT + clones revert on a non-zero -> non-zero approve; reset to 0 first.
                tx_hash, nonce = _send_signed_tx(account, chain_id, sell, oc.encode_approve(relayer, 0), nonce)
                _wait_receipt(chain_id, tx_hash)
            tx_hash, nonce = _send_signed_tx(account, chain_id, sell, oc.encode_approve(relayer, sell_atomic), nonce)
            _wait_receipt(chain_id, tx_hash)  # must be mined before the order can settle

        # 5. EIP-712-sign the GPv2 order (signed order carries appData = the bytes32 hash).
        signed_message = {
            "sellToken": sell,
            "buyToken": buy,
            "receiver": owner,  # receiver pinned to owner (drain guard)
            "sellAmount": str(sell_atomic),
            "buyAmount": str(min_buy),
            "validTo": valid_to,
            "appData": app_hash,
            "feeAmount": "0",
            "kind": "sell",
            "partiallyFillable": False,
            "sellTokenBalance": "erc20",
            "buyTokenBalance": "erc20",
        }
        typed_data = oc.build_order_typed_data(chain_id, signed_message)
        signature = _sign_typed_data(account, typed_data)

        # 6. Submit: appData on the wire is the FULL json string (+ appDataHash).
        order_body = {
            **signed_message,
            "appData": full_app_data,
            "appDataHash": app_hash,
            "signingScheme": "eip712",
            "signature": signature,
            "from": owner,
        }
        order_uid = oc.post_order(chain_id, order_body)

        return json.dumps({
            "ok": True,
            "order_uid": order_uid,
            "chain_id": chain_id,
            "owner": owner,
            "sell_token": sell,
            "buy_token": buy,
            "sell_amount": str(sell_atomic),
            "expected_buy": str(quote_buy),
            "min_buy": str(min_buy),
            "status_url": f"{oc.orderbook_url(chain_id)}/api/v1/orders/{order_uid}",
            "explorer_url": f"https://explorer.ophis.fi/orders/{order_uid}",
        })
    except Exception as exc:  # noqa: BLE001 — tool contract: return a JSON error string, never raise.
        return json.dumps({"ok": False, "error": str(exc)})


def _sign_typed_data(account, typed_data: dict) -> str:
    """EIP-712 sign with eth_account. Returns a 0x + 130-hex (65-byte) signature."""
    from eth_account.messages import encode_typed_data

    signable = encode_typed_data(full_message=typed_data)
    signed = account.sign_message(signable)
    sig = signed.signature.hex()
    return sig if sig.startswith("0x") else "0x" + sig
