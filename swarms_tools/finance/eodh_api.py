import os
import httpx
from swarms_tools.utils.formatted_string import (
    format_object_to_string,
)


def fetch_stock_news(stock_name: str):
    """
    Fetches news for a given stock from EODHD API.

    Parameters:
    stock_name (str): The name of the stock to fetch news for.
    api_key (str): The API key for EODHD API.

    Returns:
    dict: A dictionary containing the fetched news data for the specified stock.
    """
    api_key = os.getenv("EODHD_API_KEY")
    url = f"https://eodhd.com/api/news?s={stock_name}.US&offset=0&limit=10&api_token={api_key}&fmt=json"
    try:
        response = httpx.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        data = response.json()
        data = format_object_to_string(data)
        return data
    except httpx.RequestException as e:
        print(f"Failed to fetch news for {stock_name}: {e}")
        return {"error": "Failed to fetch news", "details": str(e)}


# # Example usage
# stock_name = "AAPL"
# out = fetch_stock_news(stock_name)
# print(format_object_to_string(out))
