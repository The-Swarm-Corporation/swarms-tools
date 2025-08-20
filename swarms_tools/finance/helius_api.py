import os
import httpx
from typing import Dict, Any
from loguru import logger


class HeliusAPI:
    """
    A production-grade tool for interacting with the Helius API.
    """

    BASE_URL = "https://api.helius.xyz/v0"
    API_KEY = os.getenv("HELIUS_API_KEY")

    @staticmethod
    @logger.catch
    def fetch_account_data(account: str) -> Dict[str, Any]:
        """
        Fetch data for a specific blockchain account using the Helius API.

        Args:
            account (str): The blockchain account address.

        Returns:
            Dict[str, Any]: A dictionary containing the account data.

        Raises:
            ValueError: If the account is invalid or no data is available.
            httpx.RequestException: If the API request fails.
        """
        endpoint = f"{HeliusAPI.BASE_URL}/accounts/{account}?api-key={HeliusAPI.API_KEY}"
        logger.info(f"Fetching account data for: {account}")

        try:
            response = httpx.get(endpoint, timeout=10)
            response.raise_for_status()
        except httpx.RequestException as e:
            logger.error(
                f"Failed to fetch account data from Helius API: {e}"
            )
            raise

        data = response.json()
        logger.debug(
            f"Raw data received for account {account}: {data}"
        )

        if "error" in data:
            logger.error(f"Error from Helius API: {data['error']}")
            raise ValueError(f"Helius API error: {data['error']}")

        return data

    @staticmethod
    @logger.catch
    def fetch_transaction_data(tx_signature: str) -> Dict[str, Any]:
        """
        Fetch data for a specific blockchain transaction using the Helius API.

        Args:
            tx_signature (str): The blockchain transaction signature.

        Returns:
            Dict[str, Any]: A dictionary containing the transaction data.

        Raises:
            ValueError: If the transaction signature is invalid or no data is available.
            httpx.RequestException: If the API request fails.
        """
        endpoint = f"{HeliusAPI.BASE_URL}/transactions/{tx_signature}?api-key={HeliusAPI.API_KEY}"
        logger.info(
            f"Fetching transaction data for signature: {tx_signature}"
        )

        try:
            response = httpx.get(endpoint, timeout=10)
            response.raise_for_status()
        except httpx.RequestException as e:
            logger.error(
                f"Failed to fetch transaction data from Helius API: {e}"
            )
            raise

        data = response.json()
        logger.debug(
            f"Raw data received for transaction {tx_signature}: {data}"
        )

        if "error" in data:
            logger.error(f"Error from Helius API: {data['error']}")
            raise ValueError(f"Helius API error: {data['error']}")

        return data

    @staticmethod
    @logger.catch
    def fetch_token_data(mint_address: str) -> Dict[str, Any]:
        """
        Fetch token data for a specific mint address using the Helius API.

        Args:
            mint_address (str): The blockchain mint address.

        Returns:
            Dict[str, Any]: A dictionary containing the token data.

        Raises:
            ValueError: If the mint address is invalid or no data is available.
            httpx.RequestException: If the API request fails.
        """
        endpoint = f"{HeliusAPI.BASE_URL}/tokens/{mint_address}?api-key={HeliusAPI.API_KEY}"
        logger.info(
            f"Fetching token data for mint address: {mint_address}"
        )

        try:
            response = httpx.get(endpoint, timeout=10)
            response.raise_for_status()
        except httpx.RequestException as e:
            logger.error(
                f"Failed to fetch token data from Helius API: {e}"
            )
            raise

        data = response.json()
        logger.debug(
            f"Raw data received for token {mint_address}: {data}"
        )

        if "error" in data:
            logger.error(f"Error from Helius API: {data['error']}")
            raise ValueError(f"Helius API error: {data['error']}")

        return data


def helius_api_tool(action: str, identifier: str) -> Dict[str, Any]:
    """
    A unified function to interact with the Helius API for various operations.

    Args:
        action (str): The type of action to perform ('account', 'transaction', or 'token').
        identifier (str): The identifier for the action (e.g., account address, transaction signature, or mint address).

    Returns:
        Dict[str, Any]: The data fetched from the Helius API.

    Raises:
        ValueError: If the action is invalid.
    """
    try:
        if action == "account":
            return HeliusAPI.fetch_account_data(identifier)
        elif action == "transaction":
            return HeliusAPI.fetch_transaction_data(identifier)
        elif action == "token":
            return HeliusAPI.fetch_token_data(identifier)
        else:
            raise ValueError(
                f"Invalid action: {action}. Must be 'account', 'transaction', or 'token'."
            )
    except Exception as e:
        logger.error(
            f"Error performing action '{action}' with identifier '{identifier}': {e}"
        )
        return {"error": str(e)}


# if __name__ == "__main__":
#     # Set up logging
#     logger.add("helius_api.log", rotation="500 MB", level="INFO")

#     # Example usage
#     try:
#         account_data = helius_api_tool("account", "example_account_address")
#         print("Account Data:", account_data)

#         transaction_data = helius_api_tool("transaction", "example_transaction_signature")
#         print("Transaction Data:", transaction_data)

#         token_data = helius_api_tool("token", "example_mint_address")
#         print("Token Data:", token_data)
#     except Exception as e:
#         logger.error(f"Error in Helius API tool: {e}")
