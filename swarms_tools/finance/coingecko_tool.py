import httpx
from typing import Dict, Any
from loguru import logger

from swarms_tools.utils.formatted_string import (
    format_object_to_string,
)


class CoinGeckoAPI:
    """
    A production-grade tool for fetching cryptocurrency data from CoinGecko's API.
    """

    BASE_URL = "https://api.coingecko.com/api/v3"

    @staticmethod
    @logger.catch
    def fetch_coin_data(coin_id: str) -> Dict[str, Any]:
        """
        Fetch all data about a cryptocurrency from CoinGecko.

        Args:
            coin_id (str): The unique ID of the cryptocurrency (e.g., 'bitcoin').

        Returns:
            Dict[str, Any]: A formatted dictionary containing the cryptocurrency data.

        Raises:
            ValueError: If the coin ID is invalid or data is unavailable.
            httpx.RequestException: If the API request fails.
        """
        url = f"{CoinGeckoAPI.BASE_URL}/coins/{coin_id}"
        logger.info(f"Fetching data for coin ID: {coin_id}")

        try:
            response = httpx.get(url, timeout=10)
            response.raise_for_status()
        except httpx.RequestException as e:
            logger.error(
                f"Failed to fetch data from CoinGecko API: {e}"
            )
            raise

        data = response.json()
        # logger.debug(f"Raw data received: {data}")

        if "error" in data:
            logger.error(f"Error from CoinGecko API: {data['error']}")
            raise ValueError(f"CoinGecko API error: {data['error']}")

        formatted_data = CoinGeckoAPI._format_coin_data(data)
        # logger.info(f"Formatted data for coin ID {coin_id}: {formatted_data}")
        return format_object_to_string(formatted_data)

    @staticmethod
    def _format_coin_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw cryptocurrency data into a structured dictionary.

        Args:
            data (Dict[str, Any]): Raw data from the CoinGecko API.

        Returns:
            Dict[str, Any]: Structured and formatted cryptocurrency data.
        """
        return {
            "id": data.get("id"),
            "symbol": data.get("symbol"),
            "name": data.get("name"),
            "current_price": (
                data.get("market_data", {})
                .get("current_price", {})
                .get("usd", "N/A")
            ),
            "market_cap": (
                data.get("market_data", {})
                .get("market_cap", {})
                .get("usd", "N/A")
            ),
            "total_volume": (
                data.get("market_data", {})
                .get("total_volume", {})
                .get("usd", "N/A")
            ),
            "high_24h": (
                data.get("market_data", {})
                .get("high_24h", {})
                .get("usd", "N/A")
            ),
            "low_24h": (
                data.get("market_data", {})
                .get("low_24h", {})
                .get("usd", "N/A")
            ),
            "price_change_percentage_24h": (
                data.get("market_data", {}).get(
                    "price_change_percentage_24h", "N/A"
                )
            ),
            "circulating_supply": (
                data.get("market_data", {}).get(
                    "circulating_supply", "N/A"
                )
            ),
            "total_supply": (
                data.get("market_data", {}).get("total_supply", "N/A")
            ),
            "max_supply": (
                data.get("market_data", {}).get("max_supply", "N/A")
            ),
            "last_updated": data.get("last_updated"),
            "description": (
                data.get("description", {}).get(
                    "en", "No description available."
                )
            ),
            "homepage": (
                data.get("links", {}).get(
                    "homepage", ["No homepage available"]
                )[0]
            ),
        }


def coin_gecko_coin_api(coin: str) -> Dict[str, Any]:
    """
    Fetch and display data for a specified cryptocurrency.

    Args:
        coin (str): The unique ID of the cryptocurrency (e.g., 'bitcoin').

    Returns:
        Dict[str, Any]: A formatted dictionary containing the cryptocurrency data.
    """
    try:
        coin_data = CoinGeckoAPI.fetch_coin_data(coin)
        # print(f"Data for {coin}: {coin_data}")
        return coin_data
    except Exception as e:
        logger.error(f"Error fetching data for {coin}: {e}")
        return {"error": str(e)}


# if __name__ == "__main__":
#     # Example: Fetch data for Bitcoin
#     print(coin_gecko_coin_api("bitcoin"))
