import asyncio
from datetime import datetime
from typing import Any, Dict, Optional

import aiohttp
from loguru import logger


class JupiterAPI:
    """
    A production-grade client for interacting with Jupiter's API on Solana.

    Attributes:
        base_url (str): Base URL for Jupiter API
        session (Optional[aiohttp.ClientSession]): Aiohttp session for making requests
    """

    def __init__(self):
        """Initialize the Jupiter API client."""
        self.base_url = "https://quote-api.jup.ag/v6"
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def get_price(
        self, input_mint: str, output_mint: str
    ) -> Dict[str, Any]:
        """
        Fetch real-time price data for token pairs from Jupiter.

        Args:
            input_mint (str): Input token mint address
            output_mint (str): Output token mint address

        Returns:
            Dict[str, Any]: Dictionary containing price data with the following structure:
                {
                    'data': {
                        'price': float,
                        'input_mint': str,
                        'output_mint': str,
                        'timestamp': str,
                    },
                    'success': bool
                }

        Raises:
            aiohttp.ClientError: If there's an error with the HTTP request
            ValueError: If the response is invalid
        """
        try:
            if not self.session:
                raise RuntimeError(
                    "Session not initialized. Use async context manager."
                )

            endpoint = f"/quote?inputMint={input_mint}&outputMint={output_mint}&amount=1000000000&slippageBps=50"
            url = f"{self.base_url}{endpoint}"

            logger.debug(f"Fetching price data from Jupiter: {url}")

            async with self.session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

                if not data:
                    raise ValueError(
                        "Invalid response from Jupiter API"
                    )

                result = {
                    "data": {
                        "price": (
                            float(data["outAmount"])
                            / float(data["inAmount"])
                        ),
                        "input_mint": input_mint,
                        "output_mint": output_mint,
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                    "success": True,
                }

                logger.info(
                    f"Successfully fetched price data for {input_mint}/{output_mint}"
                )
                return result

        except aiohttp.ClientError as e:
            logger.error(f"HTTP error while fetching price: {str(e)}")
            raise
        except ValueError as e:
            logger.error(
                f"Invalid response from Jupiter API: {str(e)}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error while fetching price: {str(e)}"
            )
            raise


async def get_jupiter_price_async(
    input_mint: str, output_mint: str
) -> Dict[str, Any]:
    """
    Convenience function to get price data from Jupiter without managing context.

    Args:
        input_mint (str): Input token mint address
        output_mint (str): Output token mint address

    Returns:
        Dict[str, Any]: Price data dictionary
    """
    async with JupiterAPI() as jupiter:
        return await jupiter.get_price(input_mint, output_mint)


def get_jupiter_price(
    input_mint: str, output_mint: str
) -> Dict[str, Any]:
    return asyncio.run(
        get_jupiter_price_async(input_mint, output_mint)
    )


# # Example usage:
# if __name__ == "__main__":
#     # USDC mint address on Solana
#     USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
#     # SOL mint address
#     SOL_MINT = "So11111111111111111111111111111111111111112"

#     async def main():
#         try:
#             result = await get_jupiter_price(SOL_MINT, USDC_MINT)
#             logger.info(f"Price data: {result}")
#         except Exception as e:
#             logger.error(f"Error: {str(e)}")

#     asyncio.run(main())
