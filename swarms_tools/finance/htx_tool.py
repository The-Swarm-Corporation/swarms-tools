import httpx
from loguru import logger
from swarms_tools.utils.formatted_string import (
    format_object_to_string,
)

# Configure logging
logger.add("htx_tool.log", rotation="10 MB")


def fetch_htx_data(coin_name: str) -> str:
    """
    Fetches and formats financial data for a given cryptocurrency from Huobi API.

    Parameters:
    coin_name (str): The name of the cryptocurrency to fetch data for.

    Returns:
    dict: A dictionary containing formatted data for the specified coin, including ticker, order book, recent trades, and kline data.
    """
    base_url = "https://api.huobi.pro"

    # Fetch market ticker data for the coin
    ticker_endpoint = "/market/detail/merged"
    ticker_params = {
        "symbol": f"{coin_name.lower()}usdt"
    }  # Assuming USDT pairing

    try:
        ticker_response = httpx.get(
            f"{base_url}{ticker_endpoint}",
            params=ticker_params,
        )
        ticker_response.raise_for_status()
        ticker_data = ticker_response.json()

        if ticker_data["status"] != "ok":
            logger.error(
                "Unable to fetch ticker data for coin: {}", coin_name
            )
            return {
                "error": "Unable to fetch ticker data",
                "details": ticker_data,
            }

        # Fetch order book data for the coin
        order_book_endpoint = "/market/depth"
        order_book_params = {
            "symbol": f"{coin_name.lower()}usdt",
            "type": "step0",
        }

        order_book_response = httpx.get(
            f"{base_url}{order_book_endpoint}",
            params=order_book_params,
        )
        order_book_response.raise_for_status()
        order_book_data = order_book_response.json()

        if order_book_data["status"] != "ok":
            logger.error(
                "Unable to fetch order book data for coin: {}",
                coin_name,
            )
            return {
                "error": "Unable to fetch order book data",
                "details": order_book_data,
            }

        # Fetch recent trades for the coin
        trades_endpoint = "/market/history/trade"
        trades_params = {
            "symbol": f"{coin_name.lower()}usdt",
            "size": 200,
        }

        trades_response = httpx.get(
            f"{base_url}{trades_endpoint}",
            params=trades_params,
        )
        trades_response.raise_for_status()
        trades_data = trades_response.json()

        if trades_data["status"] != "ok":
            logger.error(
                "Unable to fetch trade data for coin: {}", coin_name
            )
            return {
                "error": "Unable to fetch trade data",
                "details": trades_data,
            }

        # Fetch Kline (Candlestick) data
        kline_endpoint = "/market/history/kline"
        kline_params = {
            "symbol": f"{coin_name.lower()}usdt",
            "period": "1day",
            "size": 200,
        }

        kline_response = httpx.get(
            f"{base_url}{kline_endpoint}",
            params=kline_params,
        )
        kline_response.raise_for_status()
        kline_data = kline_response.json()

        if kline_data["status"] != "ok":
            logger.error(
                "Unable to fetch kline data for coin: {}", coin_name
            )
            return {
                "error": "Unable to fetch kline data",
                "details": kline_data,
            }

        # Format and prepare data for a single coin
        formatted_data = {
            "coin": coin_name.upper(),
            "ticker": {
                "current_price": ticker_data["tick"].get("close"),
                "high": ticker_data["tick"].get("high"),
                "low": ticker_data["tick"].get("low"),
                "open": ticker_data["tick"].get("open"),
                "volume": ticker_data["tick"].get("vol"),
                "amount": ticker_data["tick"].get("amount"),
                "count": ticker_data["tick"].get("count"),
            },
            "order_book": {
                "bids": [
                    {"price": bid[0], "amount": bid[1]}
                    for bid in order_book_data["tick"].get("bids", [])
                ],
                "asks": [
                    {"price": ask[0], "amount": ask[1]}
                    for ask in order_book_data["tick"].get("asks", [])
                ],
            },
            "recent_trades": [
                {
                    "price": trade["data"][0].get("price"),
                    "amount": trade["data"][0].get("amount"),
                    "direction": trade["data"][0].get("direction"),
                    "trade_id": trade["data"][0].get("id"),
                    "timestamp": trade["data"][0].get("ts"),
                }
                for trade in trades_data.get("data", [])
            ],
            "kline_data": [
                {
                    "timestamp": kline["id"],
                    "open": kline["open"],
                    "close": kline["close"],
                    "high": kline["high"],
                    "low": kline["low"],
                    "volume": kline["vol"],
                    "amount": kline.get("amount"),
                }
                for kline in kline_data.get("data", [])
            ],
        }

        return format_object_to_string(formatted_data)

    except httpx.RequestException as e:
        logger.error(
            "HTTP request failed for coin: {}", coin_name, exc_info=e
        )
        return {"error": "HTTP request failed", "details": str(e)}


# print(fetch_htx_data("swarms"))
