from datetime import datetime
from typing import Any, Dict

import backoff
import httpx
from loguru import logger


class GeckoTerminalAPIError(Exception):
    """Custom exception for GeckoTerminal API errors"""

    pass


@backoff.on_exception(
    backoff.expo,
    (httpx.HTTPError, GeckoTerminalAPIError),
    max_tries=3,
)
async def fetch_token_data(
    token_address: str, network: str = "ethereum", timeout: int = 30
) -> Dict[str, Any]:
    """
    Fetches comprehensive real-time data for a token from GeckoTerminal API.

    Args:
        token_address (str): The contract address of the token
        network (str, optional): Blockchain network. Defaults to "ethereum"
        timeout (int, optional): Request timeout in seconds. Defaults to 30

    Returns:
        Dict[str, Any]: Dictionary containing token data including:
            - price
            - volume
            - market cap
            - liquidity
            - price change percentages
            - trading activity

    Raises:
        GeckoTerminalAPIError: If API request fails or returns invalid data
        httpx.HTTPError: If HTTP request fails
    """
    logger.info(
        f"Fetching data for token {token_address} on {network}"
    )

    base_url = "https://api.geckoterminal.com/api/v2"
    endpoint = f"/tokens/{network}/{token_address}"

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                f"{base_url}{endpoint}",
                headers={
                    "Accept": "application/json",
                    "User-Agent": "SwarmTools/1.0",
                },
            )

            response.raise_for_status()
            data = response.json()

            if "data" not in data:
                raise GeckoTerminalAPIError(
                    "Invalid API response format"
                )

            token_data = data["data"]["attributes"]

            # Structure the response data
            processed_data = {
                "name": token_data.get("name"),
                "symbol": token_data.get("symbol"),
                "price_usd": token_data.get("price_usd"),
                "price_24h_change": token_data.get(
                    "price_24h_change"
                ),
                "volume_24h": token_data.get("volume_24h"),
                "market_cap": token_data.get("market_cap"),
                "fully_diluted_valuation": token_data.get("fdv"),
                "liquidity_usd": token_data.get("liquidity_usd"),
                "created_at": token_data.get("created_at"),
                "updated_at": datetime.utcnow().isoformat(),
                "network": network,
                "contract_address": token_address,
            }

            logger.debug(
                f"Successfully fetched data for {token_address}"
            )
            return processed_data

    except httpx.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise
    except Exception as e:
        logger.error(f"Error fetching token data: {str(e)}")
        raise GeckoTerminalAPIError(
            f"Failed to fetch token data: {str(e)}"
        )


# # Example usage
# if __name__ == "__main__":
#     import asyncio

#     async def main():
#         try:
#             # Using WETH token address as an example
#             token_address = (
#                 "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"  # WETH
#             )
#             network = "eth"  # Changed to 'eth' instead of 'ethereum'

#             logger.info("Starting token data fetch...")
#             data = await fetch_token_data(token_address, network)
#             logger.success("Successfully retrieved token data:")
#             print("\nToken Data:")
#             for key, value in data.items():
#                 print(f"{key}: {value}")

#         except GeckoTerminalAPIError as e:
#             logger.error(f"API Error: {e}")
#         except httpx.HTTPError as e:
#             logger.error(f"HTTP Error: {e}")
#         except Exception as e:
#             logger.error(f"Unexpected error: {e}")

#     asyncio.run(main())
