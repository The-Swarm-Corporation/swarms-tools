import concurrent.futures
from typing import Dict, Optional, List, Any
import requests
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
    params = {"ids": ids}
    if show_extra_info:
        params["showExtraInfo"] = "true"
    elif vs_token:
        params["vsToken"] = vs_token

    logger.info(f"Fetching Jupiter prices for: {ids}")
    resp = requests.get(f"{JUPITER_BASE}/price/v2", params=params)
    resp.raise_for_status()
    return resp.json()


def get_jupiter_metadata(mint_address: str) -> Dict[str, Any]:
    logger.info(f"Fetching Jupiter metadata for: {mint_address}")
    resp = requests.get(
        f"{JUPITER_BASE}/tokens/v1/token/{mint_address}"
    )
    resp.raise_for_status()
    return resp.json()


def get_solscan_holders(
    mint_address: str, limit: int = 10, offset: int = 0
) -> Dict[str, Any]:
    if mint_address == NATIVE_SOL_MINT:
        return {"note": "Native SOL has no holder info."}

    logger.info(f"Fetching Solscan holders for: {mint_address}")
    resp = requests.get(
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
    headers = {
        "X-API-KEY": "public"
    }  # Replace with your key if rate-limited
    url = f"{BIRDEYE_BASE}/token-price?address={mint_address}"

    logger.info(f"Fetching Birdeye price for: {mint_address}")
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_dexscreener_data(
    network: str, pair_address: str
) -> Dict[str, Any]:
    url = f"{DEXSCREENER_BASE}/pairs/{network}/{pair_address}"
    logger.info(
        f"Fetching DexScreener data for: {pair_address} on {network}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_coingecko_token_info(mint_address: str) -> Dict[str, Any]:
    logger.info(f"Fetching CoinGecko data for: {mint_address}")
    url = f"{COINGECKO_BASE}/coins/solana/contract/{mint_address}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_solanafm_token_info(mint_address: str) -> Dict[str, Any]:
    logger.info(f"Fetching SolanaFM data for: {mint_address}")
    url = f"{SOLANAFM_BASE}/accounts/{mint_address}"
    headers = {
        "accept": "application/json",
        "x-api-key": "public",  # Replace with your real key if needed
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


# ---------- Order Book Fetchers ---------- #


def get_htx_orderbook(pair: str) -> Dict[str, Any]:
    url = f"{HTX_API_BASE}/api/v1/market/orderbook"
    params = {"symbol": pair}
    logger.info(f"Fetching HTX orderbook for: {pair}")
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def get_okx_orderbook(pair: str) -> Dict[str, Any]:
    url = f"{OKX_API_BASE}/api/v5/market/orderbook"
    params = {"instId": pair}
    logger.info(f"Fetching OKX orderbook for: {pair}")
    resp = requests.get(url, params=params)
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

#     print(json.dumps(result, indent=4))
