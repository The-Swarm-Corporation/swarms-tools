from typing import Any, Dict, List, Optional

import httpx
from loguru import logger

from swarms_tools.utils.formatted_string import (
    format_object_to_string,
)

YAHOO_FINANCE_QUOTE_URL = (
    "https://query1.finance.yahoo.com/v7/finance/quote"
)


class YahooFinanceAPI:
    """
    A production-grade tool for fetching stock data from Yahoo Finance using the public API endpoint.
    """

    @staticmethod
    @logger.catch
    def fetch_stock_data(
        stock_symbols: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Fetch all possible data about one or more stocks from Yahoo Finance using the HTTP API.

        Args:
            stock_symbols (Optional[List[str]]): A list of stock symbols (e.g., ['AAPL', 'GOOG']).
                                                 If None, raises a ValueError as stocks must be specified.

        Returns:
            Dict[str, Any]: A dictionary containing the formatted stock data.

        Raises:
            ValueError: If no stock symbols are provided or the data for the symbols cannot be retrieved.
            Exception: For any other unforeseen issues.
        """
        if not stock_symbols:
            raise ValueError(
                "No stock symbols provided. Please specify at least one stock symbol."
            )

        logger.info(f"Fetching data for stocks: {stock_symbols}")

        try:
            params = {"symbols": ",".join(stock_symbols)}
            response = httpx.get(
                YAHOO_FINANCE_QUOTE_URL, params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("quoteResponse", {}).get("result", [])
            if not results:
                raise ValueError(
                    "No data returned from Yahoo Finance for the given symbols."
                )

            stock_data = {}
            for stock_info in results:
                symbol = stock_info.get("symbol", "N/A")
                formatted_data = {
                    "symbol": symbol,
                    "name": stock_info.get("shortName", "N/A"),
                    "sector": stock_info.get("sector", "N/A"),
                    "industry": stock_info.get("industry", "N/A"),
                    "current_price": stock_info.get(
                        "regularMarketPrice", "N/A"
                    ),
                    "previous_close": stock_info.get(
                        "regularMarketPreviousClose", "N/A"
                    ),
                    "open_price": stock_info.get(
                        "regularMarketOpen", "N/A"
                    ),
                    "day_high": stock_info.get(
                        "regularMarketDayHigh", "N/A"
                    ),
                    "day_low": stock_info.get(
                        "regularMarketDayLow", "N/A"
                    ),
                    "volume": stock_info.get(
                        "regularMarketVolume", "N/A"
                    ),
                    "market_cap": stock_info.get("marketCap", "N/A"),
                    "52_week_high": stock_info.get(
                        "fiftyTwoWeekHigh", "N/A"
                    ),
                    "52_week_low": stock_info.get(
                        "fiftyTwoWeekLow", "N/A"
                    ),
                    "dividend_yield": stock_info.get(
                        "dividendYield", "N/A"
                    ),
                    "description": stock_info.get(
                        "longBusinessSummary", "N/A"
                    ),
                }
                stock_data[symbol] = formatted_data

            # For any requested symbol not returned, add an error
            for symbol in stock_symbols:
                if symbol not in stock_data:
                    stock_data[symbol] = {
                        "error": "No data found for this symbol."
                    }

            return stock_data
        except Exception as e:
            logger.error(
                f"Error fetching data from Yahoo Finance API: {e}"
            )
            # Return error for all symbols if a global error occurs
            return {
                symbol: {"error": str(e)} for symbol in stock_symbols
            }


def yahoo_finance_api(
    stock_symbols: Optional[List[str]] = None,
) -> str:
    """
    Fetch and display data for one or more stocks using Yahoo Finance.

    Args:
        stock_symbols (Optional[List[str]]): A list of stock symbols to fetch data for.

    Returns:
        str: A string containing the fetched stock data.
    """
    try:
        stock_data = YahooFinanceAPI.fetch_stock_data(stock_symbols)
        return format_object_to_string(stock_data)
    except ValueError as ve:
        logger.error(f"ValueError occurred: {ve}")
        return f"error: {str(ve)}"
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return f"error: {str(e)}"
