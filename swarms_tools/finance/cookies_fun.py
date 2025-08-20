import httpx
import os
from swarms_tools.utils.formatted_string import (
    format_object_to_string,
)
from loguru import logger


class CookieFunAPIClient:
    """
    A client for interacting with the Cookie.fun API.

    This client provides functions to fetch KOL (Key Opinion Leader) data
    from the Cookie.fun platform.
    """

    def __init__(
        self, api_key: str = os.getenv("COOKIE_FUN_API_KEY")
    ):
        """
        Initialize the Cookie.fun API client.

        Args:
            api_key (str): API key for authentication. Defaults to COOKIE_FUN_API_KEY env var.
        """
        self.api_key = api_key
        self.base_url = "https://api.cookie.fun/v1"
        logger.info("Initialized CookieFunAPIClient")

    def get_kols(self, limit=50):
        """
        Fetch KOL data from Cookie.fun API.

        Args:
            limit (int): Maximum number of KOLs to retrieve. Defaults to 50.

        Returns:
            dict: JSON response containing KOL data.

        Raises:
            httpx.HTTPError: If the API request fails.
        """
        try:
            headers = {"x-api-key": self.api_key}
            logger.info(f"Fetching {limit} KOLs from Cookie.fun API")
            response = httpx.get(
                f"{self.base_url}/kols",
                headers=headers,
                params={"limit": limit},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(
                f"HTTP error occurred while fetching KOLs: {e}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while fetching KOLs: {e}"
            )
            raise


def get_kols_cookie_fun(limit: int = 50):
    """
    Helper function to fetch and format KOL data from Cookie.fun.

    Args:
        limit (int): Maximum number of KOLs to retrieve. Defaults to 50.

    Returns:
        str: Formatted string containing KOL data.

    Raises:
        httpx.HTTPError: If the API request fails.
    """
    try:
        client = CookieFunAPIClient()
        kols = client.get_kols(limit)
        logger.info(f"Successfully retrieved {len(kols)} KOLs")
        return format_object_to_string(kols)
    except Exception as e:
        logger.error(f"Error retrieving KOLs: {e}")
        raise
