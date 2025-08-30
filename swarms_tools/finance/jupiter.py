from datetime import datetime
from typing import Any, Dict
import httpx
from loguru import logger


class JupiterAPI:
    """
    A production-grade client for interacting with Jupiter's API on Solana.

    Attributes:
        base_url (str): Base URL for Jupiter API
    """

    def __init__(self):
        """Initialize the Jupiter API client."""
        self.base_url = "https://quote-api.jup.ag/v6"

    def get_price(
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
            httpx.RequestError: If there's an error with the HTTP request
            ValueError: If the response is invalid
        """
        try:
            endpoint = f"/quote?inputMint={input_mint}&outputMint={output_mint}&amount=1000000000&slippageBps=50"
            url = f"{self.base_url}{endpoint}"

            logger.debug(f"Fetching price data from Jupiter: {url}")

            response = httpx.get(url)
            response.raise_for_status()
            data = response.json()

            if not data:
                raise ValueError("Invalid response from Jupiter API")

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

        except httpx.RequestError as e:
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


def get_jupiter_price(
    input_mint: str, output_mint: str
) -> Dict[str, Any]:
    """
    Convenience function to get price data from Jupiter.

    Args:
        input_mint (str): Input token mint address
        output_mint (str): Output token mint address

    Returns:
        Dict[str, Any]: Price data dictionary
    """
    api = JupiterAPI()
    return api.get_price(input_mint, output_mint)


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
