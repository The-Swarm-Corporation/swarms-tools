"""Module for interacting with Jupiter Protocol's token and price APIs.

This module provides both synchronous and asynchronous interfaces to fetch token information
and prices from Jupiter Protocol. It uses aiohttp for optimal performance in async operations
and includes sync wrappers for backward compatibility.

Typical usage example:
    ```python
    # Async usage
    async def main():
        tokens = await fetch_all_tokens_async()
        prices = await get_token_prices_async(['SOL', 'USDC'])

    # Sync usage
    tokens = fetch_all_tokens()
    prices = get_token_prices(['SOL', 'USDC'])
    ```
"""

from typing import Dict, List, Optional, Union
import asyncio
from functools import wraps

import aiohttp
from loguru import logger

BASE_URL = "https://api.jup.ag/price/v2/"
API_BASE_URL = "https://api.jup.ag"
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "JupiterPriceAPI-Python/1.0",
}


# Reusable session for better performance
async def get_aiohttp_session():
    """Get or create an aiohttp ClientSession with connection pooling."""
    if not hasattr(get_aiohttp_session, "_session"):
        get_aiohttp_session._session = aiohttp.ClientSession(
            headers=DEFAULT_HEADERS,
            connector=aiohttp.TCPConnector(
                limit=100, ttl_dns_cache=300
            ),
        )
    return get_aiohttp_session._session


def async_to_sync(func):
    """Decorator to convert an async function to sync function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


async def jupiter_fetch_token_by_mint_address_async(
    mint_address: str,
) -> Dict:
    """Asynchronously fetch token information by mint address.

    Args:
        mint_address: The mint address of the token to fetch.

    Returns:
        Dict containing token information.

    Raises:
        aiohttp.ClientError: If the API request fails.
    """
    session = await get_aiohttp_session()
    url = f"{API_BASE_URL}/tokens/v1/token/{mint_address}"

    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()


@async_to_sync
async def jupiter_fetch_token_by_mint_address(
    mint_address: str,
) -> Dict:
    """Synchronous wrapper for fetch_token_by_mint_address_async."""
    return await jupiter_fetch_token_by_mint_address_async(
        mint_address
    )


async def jupiter_fetch_tradable_tokens_async() -> List[Dict]:
    """Asynchronously fetch list of tradable tokens.

    Returns:
        List of dictionaries containing tradable token information.

    Raises:
        aiohttp.ClientError: If the API request fails.
    """
    session = await get_aiohttp_session()
    url = f"{API_BASE_URL}/tokens/v1/mints/tradable"

    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()


@async_to_sync
async def jupiter_fetch_tradable_tokens() -> List[Dict]:
    """Synchronous wrapper for fetch_tradable_tokens_async."""
    return await jupiter_fetch_tradable_tokens_async()


async def jupiter_get_token_prices_async(
    token_ids: Union[str, List[str]],
    vs_token: Optional[str] = None,
    show_extra_info: bool = False,
) -> Dict:
    """Asynchronously get prices for specified tokens from Jupiter Price API.

    Args:
        token_ids: Single token ID or list of token IDs (will be comma-separated)
        vs_token: Optional token to denominate prices in (e.g. SOL mint address)
        show_extra_info: Whether to show additional price information

    Returns:
        Dict containing price data for requested tokens

    Raises:
        aiohttp.ClientError: If the API request fails
        ValueError: If invalid parameter combination is provided
    """
    try:
        # Convert list of tokens to comma-separated string if needed
        if isinstance(token_ids, list):
            token_ids = ",".join(token_ids)

        # Build query parameters
        params = {"ids": token_ids}
        if vs_token and show_extra_info:
            raise ValueError(
                "Cannot use vs_token and show_extra_info parameters together"
            )

        if vs_token:
            params["vsToken"] = vs_token
        if show_extra_info:
            params["showExtraInfo"] = "true"

        # Make API request
        logger.debug(
            f"Making request to Jupiter Price API with params: {params}"
        )
        session = await get_aiohttp_session()

        async with session.get(BASE_URL, params=params) as response:
            response.raise_for_status()
            return await response.json()

    except aiohttp.ClientError as e:
        logger.error(
            f"Failed to fetch prices from Jupiter API: {str(e)}"
        )
        raise
    except ValueError as e:
        logger.error(
            f"Failed to parse Jupiter API response: {str(e)}"
        )
        raise


@async_to_sync
async def jupiter_get_token_prices(
    token_ids: Union[str, List[str]],
    vs_token: Optional[str] = None,
    show_extra_info: bool = False,
) -> Dict:
    """Synchronous wrapper for get_token_prices_async."""
    return await jupiter_get_token_prices_async(
        token_ids, vs_token, show_extra_info
    )


async def jupiter_fetch_all_tokens_async() -> List[Dict]:
    """Asynchronously fetch all available tokens.

    Returns:
        List of dictionaries containing token information.

    Raises:
        aiohttp.ClientError: If the API request fails.
    """
    session = await get_aiohttp_session()
    url = f"{API_BASE_URL}/tokens/v1/all"

    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()


@async_to_sync
async def jupiter_fetch_all_tokens() -> List[Dict]:
    """Synchronous wrapper for fetch_all_tokens_async."""
    return await jupiter_fetch_all_tokens_async()


async def cleanup():
    """Cleanup function to close the aiohttp session."""
    if hasattr(get_aiohttp_session, "_session"):
        await get_aiohttp_session._session.close()


# if __name__ == "__main__":
#     # Test the async functions
#     print(fetch_tradable_tokens())
