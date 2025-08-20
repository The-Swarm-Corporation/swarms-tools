import concurrent.futures
from typing import Any, Dict, List, Optional

import httpx
from loguru import logger

# Constants
JUPITER_BASE = "https://lite-api.jup.ag"
SOLSCAN_BASE = "https://public-api.solscan.io"
BIRDEYE_BASE = "https://public-api.birdeye.so/defi"
DEXSCREENER_BASE = "https://api.dexscreener.com/latest/dex"
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
SOLANAFM_BASE = "https://api.solana.fm/v0"
HTX_API_BASE = "https://api.htx.com"
OKX_API_BASE = "https://www.okx.com"
NATIVE_SOL_MINT = "So11111111111111111111111111111111111111112"


# ---------- Modular Data Source Fetchers ---------- #


def safe_fetch(fn, *args, **kwargs) -> Dict[str, Any]:
    """
    Safely executes a function and catches any exceptions, returning an error dict if failed.

    Args:
        fn (callable): The function to execute.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        Dict[str, Any]: The result of the function call, or an error dictionary if an exception occurs.
    """
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.error(f"{fn.__name__} failed: {e}")
        return {"error": f"{fn.__name__} failed", "details": str(e)}


def get_jupiter_price(
    ids: str,
    vs_token: Optional[str] = None,
    show_extra_info: bool = False,
) -> Dict[str, Any]:
    """
    Fetches price data for one or more Solana tokens from the Jupiter API.

    Args:
        ids (str): Comma-separated list of token mint addresses.
        vs_token (Optional[str], optional): The mint address of the token to compare against. Defaults to None.
        show_extra_info (bool, optional): Whether to include extra info in the response. Defaults to False.

    Returns:
        Dict[str, Any]: The JSON response from the Jupiter API containing price data.
    """
    params = {"ids": ids}
    if show_extra_info:
        params["showExtraInfo"] = "true"
    elif vs_token:
        params["vsToken"] = vs_token

    logger.info(f"Fetching Jupiter prices for: {ids}")
    resp = httpx.get(f"{JUPITER_BASE}/price/v2", params=params)
    resp.raise_for_status()
    return resp.json()


def get_jupiter_metadata(mint_address: str) -> Dict[str, Any]:
    """
    Fetches metadata for a Solana token from the Jupiter API.

    Args:
        mint_address (str): The mint address of the token.

    Returns:
        Dict[str, Any]: The JSON response from the Jupiter API containing token metadata.
    """
    logger.info(f"Fetching Jupiter metadata for: {mint_address}")
    resp = httpx.get(f"{JUPITER_BASE}/tokens/v1/token/{mint_address}")
    resp.raise_for_status()
    return resp.json()


def get_solscan_holders(
    mint_address: str, limit: int = 10, offset: int = 0
) -> Dict[str, Any]:
    """
    Fetches holder information for a Solana token from the Solscan API.

    Args:
        mint_address (str): The mint address of the token.
        limit (int, optional): Number of holders to fetch. Defaults to 10.
        offset (int, optional): Offset for pagination. Defaults to 0.

    Returns:
        Dict[str, Any]: The JSON response from the Solscan API containing holder data,
                        or a note if the token is native SOL.
    """
    if mint_address == NATIVE_SOL_MINT:
        return {"note": "Native SOL has no holder info."}

    logger.info(f"Fetching Solscan holders for: {mint_address}")
    resp = httpx.get(
        f"{SOLSCAN_BASE}/token/holders",
        params={
            "tokenAddress": mint_address,
            "limit": limit,
            "offset": offset,
        },
    )
    resp.raise_for_status()
    return resp.json()


def get_birdeye_price(mint_address: str) -> Dict[str, Any]:
    """
    Fetches the price of a Solana token from the Birdeye API.

    Args:
        mint_address (str): The mint address of the token.

    Returns:
        Dict[str, Any]: The JSON response from the Birdeye API containing price data.
    """
    headers = {
        "X-API-KEY": "public"
    }  # Replace with your key if rate-limited
    url = f"{BIRDEYE_BASE}/token-price?address={mint_address}"

    logger.info(f"Fetching Birdeye price for: {mint_address}")
    resp = httpx.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_dexscreener_data(
    network: str, pair_address: str
) -> Dict[str, Any]:
    """
    Fetches DEX pair data from the DexScreener API.

    Args:
        network (str): The blockchain network (e.g., "solana").
        pair_address (str): The address of the DEX pair.

    Returns:
        Dict[str, Any]: The JSON response from the DexScreener API containing pair data.
    """
    url = f"{DEXSCREENER_BASE}/pairs/{network}/{pair_address}"
    logger.info(
        f"Fetching DexScreener data for: {pair_address} on {network}"
    )
    resp = httpx.get(url)
    resp.raise_for_status()
    return resp.json()


def get_coingecko_token_info(mint_address: str) -> Dict[str, Any]:
    """
    Fetches token information from the CoinGecko API for a Solana token.

    Args:
        mint_address (str): The mint address of the token.

    Returns:
        Dict[str, Any]: The JSON response from the CoinGecko API containing token info.
    """
    logger.info(f"Fetching CoinGecko data for: {mint_address}")
    url = f"{COINGECKO_BASE}/coins/solana/contract/{mint_address}"
    resp = httpx.get(url)
    resp.raise_for_status()
    return resp.json()


def get_solanafm_token_info(mint_address: str) -> Dict[str, Any]:
    """
    Fetches token information from the SolanaFM API for a Solana token.

    Args:
        mint_address (str): The mint address of the token.

    Returns:
        Dict[str, Any]: The JSON response from the SolanaFM API containing token info.
    """
    logger.info(f"Fetching SolanaFM data for: {mint_address}")
    url = f"{SOLANAFM_BASE}/accounts/{mint_address}"
    headers = {
        "accept": "application/json",
        "x-api-key": "public",  # Replace with your real key if needed
    }
    resp = httpx.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


# ---------- Order Book Fetchers ---------- #


def get_htx_orderbook(pair: str) -> Dict[str, Any]:
    """
    Fetches the order book for a trading pair from the HTX (Huobi) API.

    Args:
        pair (str): The trading pair symbol (e.g., "solusdt").

    Returns:
        Dict[str, Any]: The JSON response from the HTX API containing order book data.
    """
    url = f"{HTX_API_BASE}/api/v1/market/orderbook"
    params = {"symbol": pair}
    logger.info(f"Fetching HTX orderbook for: {pair}")
    resp = httpx.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def get_okx_orderbook(pair: str) -> Dict[str, Any]:
    """
    Fetches the order book for a trading pair from the OKX API.

    Args:
        pair (str): The trading pair instrument ID (e.g., "SOL-USDT").

    Returns:
        Dict[str, Any]: The JSON response from the OKX API containing order book data.
    """
    url = f"{OKX_API_BASE}/api/v5/market/orderbook"
    params = {"instId": pair}
    logger.info(f"Fetching OKX orderbook for: {pair}")
    resp = httpx.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


# ---------- Aggregator Core ---------- #


def fetch_solana_coin_info(
    ids: str,
    vs_token: Optional[str] = None,
    show_extra_info: bool = False,
    limit: int = 10,
    offset: int = 0,
    network: str = "solana",
    dex_pair_address: Optional[str] = None,
    coin_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Aggregates Solana token information from multiple sources concurrently.

    Args:
        ids (str): Comma-separated list of token mint addresses.
        vs_token (Optional[str], optional): The mint address of the token to compare against. Defaults to None.
        show_extra_info (bool, optional): Whether to include extra info in the Jupiter price response. Defaults to False.
        limit (int, optional): Number of holders to fetch from Solscan. Defaults to 10.
        offset (int, optional): Offset for Solscan holders pagination. Defaults to 0.
        network (str, optional): Blockchain network for DEX Screener. Defaults to "solana".
        dex_pair_address (Optional[str], optional): DEX pair address for fetching DEX Screener data. Defaults to None.
        coin_name (Optional[str], optional): Optional coin name (unused). Defaults to None.

    Returns:
        Dict[str, Any]: Aggregated token information from various APIs.
    """
    ids_list: List[str] = ids.split(",")
    first_token: str = ids_list[0]

    # Define tasks to be executed concurrently
    tasks = {
        "jupiterPrice": (
            get_jupiter_price,
            (ids, vs_token, show_extra_info),
        ),
        "tokenMetadata": (get_jupiter_metadata, (first_token,)),
        "tokenHolders": (
            get_solscan_holders,
            (first_token, limit, offset),
        ),
        # Uncomment these if you want to include other API calls
        # "birdeye": (get_birdeye_price, (first_token,)),
        # "coingecko": (get_coingecko_token_info, (first_token,)),
        # "solanafm": (get_solanafm_token_info, (first_token,)),
    }

    result = {
        "success": True,
        "tokenIds": ids_list,
    }

    # Execute tasks concurrently
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(tasks)
    ) as executor:
        # Submit all tasks
        future_to_key = {
            executor.submit(safe_fetch, fn, *args): key
            for key, (fn, args) in tasks.items()
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_key):
            key = future_to_key[future]
            result[key] = future.result()

    # Add conditional API calls if needed
    if dex_pair_address:
        result["dexscreener"] = safe_fetch(
            get_dexscreener_data, network, dex_pair_address
        )

    return result


# # ---------- Example CLI Usage ---------- #

# if __name__ == "__main__":

#     result = fetch_solana_coin_info(
#         ids="74SBV4zDXxTRgv1pEMoECskKBkZHc2yGPnc7GYVepump",  # Example token address
#         show_extra_info=True,
#     )

#     print(orjson.dumps(result, option=orjson.OPT_INDENT_2).decode())
