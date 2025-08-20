import os
import httpx
from typing import List, Dict, Any, Optional
from loguru import logger
from swarms_tools.utils.formatted_string import (
    format_object_to_string,
)


class OKXAPI:
    """
    A production-grade tool for interacting with the OKX API to fetch coin data.
    """

    BASE_URL = "https://www.okx.com/api/v5"
    API_KEY = os.getenv("OKX_API_KEY")
    API_SECRET = os.getenv(
        "OKX_API_SECRET"
    )  # Fetch API secret from environment variable
    PASSPHRASE = os.getenv(
        "OKX_PASSPHRASE"
    )  # Fetch passphrase from environment variable

    @staticmethod
    @logger.catch
    def fetch_coin_data(
        coin_symbols: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Fetch all possible data about one or more coins from OKX.

        Args:
            coin_symbols (Optional[List[str]]): A list of coin symbols (e.g., ['BTC-USDT', 'ETH-USDT']).
                                                 If None, fetches data for all available coins.

        Returns:
            Dict[str, Any]: A dictionary containing the formatted coin data.

        Raises:
            ValueError: If the API response contains errors or the coin symbols are invalid.
            httpx.RequestException: If the API request fails.
        """
        endpoint = f"{OKXAPI.BASE_URL}/market/tickers"
        params = {"instType": "SPOT"}
        logger.info(
            f"Fetching coin data for: {coin_symbols or 'all available coins'}"
        )

        try:
            response = httpx.get(endpoint, params=params)
            response.raise_for_status()
        except httpx.RequestException as e:
            logger.error(
                f"Failed to fetch coin data from OKX API: {e}"
            )
            raise

        data = response.json()
        logger.debug(f"Raw data received: {data}")

        if data.get("code") != "0":
            logger.error(
                f"Error from OKX API: {data.get('msg', 'Unknown error')}"
            )
            raise ValueError(
                f"OKX API error: {data.get('msg', 'Unknown error')}"
            )

        filtered_data = OKXAPI._filter_data(
            data["data"], coin_symbols
        )
        logger.info(f"Filtered data: {filtered_data}")
        return filtered_data

    @staticmethod
    def _filter_data(
        data: List[Dict[str, Any]], coin_symbols: Optional[List[str]]
    ) -> Dict[str, Any]:
        """
        Filter raw API data for specific coin symbols or return all available data.

        Args:
            data (List[Dict[str, Any]]): The raw data from the OKX API.
            coin_symbols (Optional[List[str]]): A list of coin symbols to filter data for.

        Returns:
            Dict[str, Any]: A dictionary of filtered coin data.
        """
        if not coin_symbols:
            return {coin["instId"]: coin for coin in data}

        filtered_data = {
            coin["instId"]: coin
            for coin in data
            if coin["instId"] in coin_symbols
        }
        if not filtered_data:
            logger.warning(
                f"No data found for specified coin symbols: {coin_symbols}"
            )
        return filtered_data


def okx_api_tool(coin_symbols: Optional[List[str]] = None) -> str:
    """
    Fetch and display data for one or more coins using the OKX API.

    Args:
        coin_symbols (Optional[List[str]]): A list of coin symbols to fetch data for.

    Returns:
       String: A string containing the fetched coin data.
    """
    try:
        coin_data = OKXAPI.fetch_coin_data(coin_symbols)
        return format_object_to_string(coin_data)
    except ValueError as ve:
        logger.error(f"ValueError occurred: {ve}")
        return {"error": str(ve)}
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return {"error": str(e)}


# if __name__ == "__main__":
#     # Set up logging
#     logger.add("okx_api_tool.log", rotation="500 MB", level="INFO")

#     # Example usage
#     try:
#         # Fetch data for a single coin
#         single_coin = okx_api_tool(["BTC-USDT"])
#         print("Single Coin Data:", single_coin)

#         # Fetch data for multiple coins
#         multiple_coins = okx_api_tool(["BTC-USDT", "ETH-USDT"])
#         print("Multiple Coins Data:", multiple_coins)

#         # Fetch data for all coins
#         all_coins = okx_api_tool()
#         print("All Coins Data:", all_coins)
#     except Exception as e:
#         logger.error(f"Error in OKX API tool: {e}")
