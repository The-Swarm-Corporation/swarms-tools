import httpx
import os


class SolanaWalletBalanceChecker:
    def __init__(
        self,
        api_key: str = os.getenv("HELIUS_API_KEY"),
        base_url: str = "https://api.helius.xyz/v0/addresses/",
    ):
        """
        Initializes the Solana wallet balance checker using Hélius API.

        Args:
            api_key (str): Your Hélius API key.
            base_url (str): The base URL for the Hélius API.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.token_mapping = self.load_token_list()

    def load_token_list(self) -> dict:
        """
        Loads the Solana token list to map mint addresses to token names.

        Returns:
            dict: A dictionary mapping mint addresses to token names.
        """
        url = "https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            token_list = response.json()["tokens"]
            return {
                token["address"]: token["symbol"]
                for token in token_list
            }
        except httpx.RequestException as e:
            print(f"Error fetching token list: {e}")
            return {}

    def get_wallet_balances(self, wallet_address: str) -> dict:
        """
        Fetches the SOL and SPL token balances for the given wallet address.

        Args:
            wallet_address (str): The public key of the wallet.

        Returns:
            dict: A dictionary containing SOL and SPL token balances.
        """
        url = f"{self.base_url}{wallet_address}/balances?api-key={self.api_key}"
        try:
            response = httpx.get(url)
            response.raise_for_status()  # Ensure the request was successful
            return response.json()
        except httpx.RequestException as e:
            print(f"Error fetching wallet balances: {e}")
            return None

    def display_balances(self, wallet_address: str) -> None:
        """
        Fetches and displays the SOL and SPL token balances with token names.

        Args:
            wallet_address (str): The public key of the wallet.
        """
        print(f"Fetching balances for wallet: {wallet_address}")
        balances_data = self.get_wallet_balances(wallet_address)

        if not balances_data:
            print("No balance data found or API request failed.")
            return

        # Display SOL balance
        sol_balance = (
            balances_data.get("nativeBalance", 0) / 1e9
        )  # Convert lamports to SOL
        print(f"SOL: {sol_balance}")

        # Display SPL token balances
        tokens = balances_data.get("tokens", [])
        if not tokens:
            print("No SPL tokens found.")
        else:
            print("SPL Tokens:")
            for token in tokens:
                mint = token.get("mint")
                amount = token.get("amount", 0)
                decimals = token.get("decimals", 0)
                balance = amount / (10**decimals)
                token_name = self.token_mapping.get(
                    mint, "Unknown Token"
                )
                print(f"  {token_name} ({mint}): {balance}")


def check_solana_balance(wallet_address: str) -> str:
    """
    Checks and returns the SOL and SPL token balances for a given Solana wallet address.

    Args:
        wallet_address (str): The public key of the Solana wallet.

    Returns:
        str: A string representation of the SOL and SPL token balances.

    Raises:
        ValueError: If the wallet_address is not a string.
        TypeError: If the wallet_address is not a valid Solana wallet address.
    """
    try:
        checker = SolanaWalletBalanceChecker(
            api_key=os.getenv("HELIUS_API_KEY")
        )
        balance_info = checker.display_balances(wallet_address)
        return str(balance_info)
    except Exception as e:
        raise TypeError(
            f"Invalid wallet_address: {wallet_address}. Error: {e}"
        )


def check_multiple_wallets(wallet_addresses: list[str]) -> str:
    """
    Checks and returns the SOL and SPL token balances for multiple Solana wallet addresses.

    Args:
        wallet_addresses (list[str]): A list of public keys of the Solana wallets.

    Returns:
        list[str]: A list of string representations of the SOL and SPL token balances for each wallet address.

    Raises:
        ValueError: If any wallet_address in the list is not a string.
        TypeError: If any wallet_address in the list is not a valid Solana wallet address.
    """
    out = [
        check_solana_balance(wallet_address)
        for wallet_address in wallet_addresses
    ]
    return str(out)
