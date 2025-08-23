import os
import httpx
from typing import Dict, Any, Optional
from loguru import logger
from swarms_tools.utils.formatted_string import (
    format_object_to_string,
)

from typing import List


class CoinMarketCapAPI:
    """
    A production-grade tool for fetching cryptocurrency data from CoinMarketCap's API.
    """

    BASE_URL = "https://pro-api.coinmarketcap.com/v1"
    API_KEY = os.getenv(
        "COINMARKETCAP_API_KEY"
    )  # Replace with your actual API key

    @staticmethod
    @logger.catch
    def fetch_coin_data(
        coin_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Fetch all possible data about one or more cryptocurrencies from CoinMarketCap.

        Args:
            coin_names (Optional[List[str]]): A list of coin names to fetch data for (e.g., ['Bitcoin', 'Ethereum']).
                                              If None, fetches data for all available coins.

        Returns:
            Dict[str, Any]: A dictionary containing the fetched cryptocurrency data.

        Raises:
            ValueError: If the API response contains errors or if the coin names are invalid.
            httpx.RequestException: If the API request fails.
        """
        endpoint = f"{CoinMarketCapAPI.BASE_URL}/cryptocurrency/listings/latest"
        headers = {"X-CMC_PRO_API_KEY": CoinMarketCapAPI.API_KEY}
        logger.info(
            f"Fetching data from CoinMarketCap for coins: {coin_names or 'all available coins'}"
        )

        try:
            response = httpx.get(endpoint, headers=headers)
            response.raise_for_status()
        except httpx.RequestException as e:
            logger.error(
                f"Failed to fetch data from CoinMarketCap API: {e}"
            )
            raise

        data = response.json()
        logger.debug(f"Raw data received: {data}")

        if data.get("status", {}).get("error_code") != 0:
            logger.error(
                f"Error from CoinMarketCap API: {data['status'].get('error_message', 'Unknown error')}"
            )
            raise ValueError(
                f"CoinMarketCap API error: {data['status'].get('error_message', 'Unknown error')}"
            )

        filtered_data = CoinMarketCapAPI._filter_data(
            data["data"], coin_names
        )
        logger.info(f"Filtered data: {filtered_data}")
        return filtered_data

    @staticmethod
    def _filter_data(
        data: List[Dict[str, Any]], coin_names: Optional[List[str]]
    ) -> Dict[str, Any]:
        """
        Filter raw API data for specific coin names or return all available data.

        Args:
            data (List[Dict[str, Any]]): The raw data from the CoinMarketCap API.
            coin_names (Optional[List[str]]): A list of coin names to filter data for.

        Returns:
            Dict[str, Any]: A dictionary of filtered cryptocurrency data.
        """
        if not coin_names:
            return {coin["name"]: coin for coin in data}

        filtered_data = {
            coin["name"]: coin
            for coin in data
            if coin["name"].lower()
            in {name.lower() for name in coin_names}
        }
        if not filtered_data:
            logger.warning(
                f"No data found for specified coin names: {coin_names}"
            )
        return filtered_data


def coinmarketcap_api(
    coin_names: Optional[List[str]] = None,
) -> str:
    """
    Fetch and display data for one or more cryptocurrencies using CoinMarketCap.

    Args:
        coin_names (Optional[List[str]]): A list of coin names to fetch data for.

    Returns:
        str: A str of fetched cryptocurrency data.
    """
    try:
        coin_data = CoinMarketCapAPI.fetch_coin_data(coin_names)
        return format_object_to_string(coin_data)
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return {"error": str(e)}


# if __name__ == "__main__":
#     # Set up logging
#     logger.add("coinmarketcap_api.log", rotation="500 MB", level="INFO")

#     # Example usage
#     single_coin = coinmarketcap_api(["Bitcoin"])
#     print("Single Coin Data:", single_coin)

#     multiple_coins = coinmarketcap_api(["Bitcoin", "Ethereum", "Tether"])
#     print("Multiple Coins Data:", multiple_coins)

#     all_coins = coinmarketcap_api()
#     print("All Coins Data:", all_coins)
