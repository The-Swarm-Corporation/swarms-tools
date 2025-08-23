import base64
import hashlib
import hmac
import orjson
import httpx
import time
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Union

# requests import removed - using httpx instead
from loguru import logger
from swarms_tools.utils.formatted_string import (
    format_object_to_string,
)
import os

# Constants
BASE_URL = "https://api.pro.coinbase.com"
SANDBOX_URL = "https://api-public.sandbox.pro.coinbase.com"


def create_auth_headers(
    method: str, request_path: str, body: str = ""
) -> Dict[str, str]:
    """
    Create authentication headers for Coinbase API requests.

    Args:
        method: HTTP method
        request_path: API endpoint path
        body: Request body for POST requests

    Returns:
        Dictionary of authentication headers
    """
    api_key = os.getenv("COINBASE_API_KEY")
    api_secret = os.getenv("COINBASE_API_SECRET")
    passphrase = os.getenv("COINBASE_API_PASSPHRASE")
    timestamp = str(time.time())
    message = timestamp + method + request_path + (body or "")
    hmac_key = base64.b64decode(api_secret)
    signature = hmac.new(
        hmac_key, message.encode("utf-8"), hashlib.sha256
    )
    signature_b64 = base64.b64encode(signature.digest()).decode(
        "utf-8"
    )

    return {
        "CB-ACCESS-KEY": api_key,
        "CB-ACCESS-SIGN": signature_b64,
        "CB-ACCESS-TIMESTAMP": timestamp,
        "CB-ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json",
    }


def get_coin_data(
    symbol: str, sandbox: bool = False
) -> Dict[str, Any]:
    """
    Fetch comprehensive data about a cryptocurrency.

    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        sandbox: Whether to use sandbox environment

    Returns:
        Dictionary containing coin data including price, volume, market data

    Raises:
        ValueError: If the symbol is invalid
        httpx.RequestException: For API errors
    """
    try:
        if "-" not in symbol:
            raise ValueError(
                f"Invalid symbol format: {symbol}. Expected format: 'BTC-USD'"
            )

        base_url = SANDBOX_URL if sandbox else BASE_URL
        logger.info(f"Fetching data for {symbol}")

        # Get ticker data
        ticker_response = httpx.get(
            f"{base_url}/products/{symbol}/ticker"
        )
        ticker_response.raise_for_status()
        ticker = ticker_response.json()

        # Get 24h stats
        stats_response = httpx.get(
            f"{base_url}/products/{symbol}/stats"
        )
        stats_response.raise_for_status()
        stats = stats_response.json()

        # Format the response
        coin_data = {
            "symbol": symbol,
            "price": {
                "current": Decimal(str(ticker.get("price", "0"))),
                "bid": Decimal(str(ticker.get("bid", "0"))),
                "ask": Decimal(str(ticker.get("ask", "0"))),
            },
            "volume": {
                "24h": Decimal(str(stats.get("volume", "0"))),
                "last_trade": Decimal(str(ticker.get("volume", "0"))),
            },
            "market_data": {
                "24h_high": Decimal(str(stats.get("high", "0"))),
                "24h_low": Decimal(str(stats.get("low", "0"))),
                "24h_open": Decimal(str(stats.get("open", "0"))),
            },
            "timestamp": datetime.now().isoformat(),
            "raw_data": {"ticker": ticker, "stats": stats},
        }

        logger.success(f"Successfully fetched data for {symbol}")
        return format_object_to_string(coin_data)

    except httpx.RequestException as e:
        logger.error(
            f"API error fetching data for {symbol}: {str(e)}"
        )
        raise
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        raise


def place_buy_order(
    symbol: str,
    amount: Union[str, float, Decimal],
    sandbox: bool = False,
) -> Dict[str, Any]:
    """
    Place a market buy order for a cryptocurrency.

    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        amount: Amount to buy (in quote currency for market orders)
        api_key: Coinbase API key
        api_secret: Coinbase API secret
        passphrase: Coinbase API passphrase
        sandbox: Whether to use sandbox environment

    Returns:
        Order details from Coinbase
    """
    try:
        base_url = SANDBOX_URL if sandbox else BASE_URL
        endpoint = "/orders"

        order_data = {
            "product_id": symbol,
            "side": "buy",
            "type": "market",
            "funds": str(amount),
        }

        headers = create_auth_headers(
            "POST", endpoint, orjson.dumps(order_data).decode()
        )

        logger.info(f"Placing buy order for {amount} {symbol}")
        response = httpx.post(
            f"{base_url}{endpoint}", headers=headers, json=order_data
        )
        response.raise_for_status()

        order = response.json()
        logger.success(f"Successfully placed buy order for {symbol}")
        return format_object_to_string(order)

    except httpx.RequestException as e:
        logger.error(
            f"API error placing buy order for {symbol}: {str(e)}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Error placing buy order for {symbol}: {str(e)}"
        )
        raise


def place_sell_order(
    symbol: str,
    amount: Union[str, float, Decimal],
    sandbox: bool = False,
) -> Dict[str, Any]:
    """
    Place a market sell order for a cryptocurrency.

    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        amount: Amount to sell (in base currency)
        sandbox: Whether to use sandbox environment

    Returns:
        Order details from Coinbase
    """
    try:
        base_url = SANDBOX_URL if sandbox else BASE_URL
        endpoint = "/orders"

        order_data = {
            "product_id": symbol,
            "side": "sell",
            "type": "market",
            "size": str(amount),
        }

        headers = create_auth_headers(
            "POST", endpoint, orjson.dumps(order_data).decode()
        )

        logger.info(f"Placing sell order for {amount} {symbol}")
        response = httpx.post(
            f"{base_url}{endpoint}", headers=headers, json=order_data
        )
        response.raise_for_status()

        order = response.json()
        logger.success(f"Successfully placed sell order for {symbol}")
        return format_object_to_string(order)

    except httpx.RequestException as e:
        logger.error(
            f"API error placing sell order for {symbol}: {str(e)}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Error placing sell order for {symbol}: {str(e)}"
        )
        raise
