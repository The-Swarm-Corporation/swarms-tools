import subprocess
from typing import Any, Dict, List, Optional
import httpx

try:
    from web3 import Web3
except ImportError:
    subprocess.run(["pip", "install", "web3"])
    from web3 import Web3

from loguru import logger

RPC_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
UNISWAP_SUBGRAPH_URL = (
    "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
)


class UniswapDataFetcher:
    def __init__(self, rpc_url: str, uniswap_subgraph_url: str):
        """
        Initialize the UniswapDataFetcher.

        Args:
            rpc_url (str): The RPC URL of the Ethereum node.
            uniswap_subgraph_url (str): The URL of the Uniswap subgraph API.
        """
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.subgraph_url = uniswap_subgraph_url

        if not self.web3.isConnected():
            logger.error("Failed to connect to Ethereum node.")
            raise ConnectionError(
                "Unable to connect to Ethereum node."
            )

        logger.info("Connected to Ethereum node.")

    def fetch_pair_data(
        self, token0: str, token1: str
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch pair data from the Uniswap subgraph.

        Args:
            token0 (str): The address of the first token in the pair.
            token1 (str): The address of the second token in the pair.

        Returns:
            Optional[Dict[str, Any]]: Pair data if found, otherwise None.
        """
        query = {
            "query": (
                """
            query ($token0: String!, $token1: String!) {
                pairs(where: {token0: $token0, token1: $token1}) {
                    id
                    reserve0
                    reserve1
                    totalSupply
                    volumeToken0
                    volumeToken1
                }
            }
            """
            ),
            "variables": {
                "token0": token0.lower(),
                "token1": token1.lower(),
            },
        }

        logger.info(
            "Fetching pair data for token pair: {} - {}",
            token0,
            token1,
        )
        response = httpx.post(self.subgraph_url, json=query)
        response.raise_for_status()

        data = response.json()
        return data.get("data", {}).get("pairs", [None])[0]

    def fetch_token_data(
        self, token_address: str
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch token data from the Uniswap subgraph.

        Args:
            token_address (str): The address of the token.

        Returns:
            Optional[Dict[str, Any]]: Token data if found, otherwise None.
        """
        query = {
            "query": (
                """
            query ($address: String!) {
                token(id: $address) {
                    id
                    symbol
                    name
                    decimals
                    totalSupply
                }
            }
            """
            ),
            "variables": {"address": token_address.lower()},
        }

        logger.info(
            "Fetching token data for address: {}", token_address
        )
        response = httpx.post(self.subgraph_url, json=query)
        response.raise_for_status()

        data = response.json()
        return data.get("data", {}).get("token")

    def fetch_pool_volume(self, pool_address: str) -> Optional[float]:
        """
        Fetch the 24-hour volume of a specific pool.

        Args:
            pool_address (str): The address of the pool.

        Returns:
            Optional[float]: The 24-hour volume of the pool if available, otherwise None.
        """
        query = {
            "query": (
                """
            query ($address: String!) {
                pair(id: $address) {
                    volumeUSD
                }
            }
            """
            ),
            "variables": {"address": pool_address.lower()},
        }

        logger.info(
            "Fetching pool volume for address: {}", pool_address
        )
        response = httpx.post(self.subgraph_url, json=query)
        response.raise_for_status()

        data = response.json()
        volume = data.get("data", {}).get("pair", {}).get("volumeUSD")
        return float(volume) if volume else None

    def fetch_liquidity_positions(
        self, user_address: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch liquidity positions of a user.

        Args:
            user_address (str): The address of the user.

        Returns:
            Optional[List[Dict[str, Any]]]: A list of liquidity positions if available, otherwise None.
        """
        query = {
            "query": (
                """
            query ($address: String!) {
                user(id: $address) {
                    liquidityPositions {
                        id
                        pair {
                            id
                            token0 {
                                symbol
                            }
                            token1 {
                                symbol
                            }
                        }
                        liquidityTokenBalance
                    }
                }
            }
            """
            ),
            "variables": {"address": user_address.lower()},
        }

        logger.info(
            "Fetching liquidity positions for user: {}", user_address
        )
        response = httpx.post(self.subgraph_url, json=query)
        response.raise_for_status()

        data = response.json()
        user_data = data.get("data", {}).get("user")
        return (
            user_data.get("liquidityPositions") if user_data else None
        )


def fetch_token_data(token: str) -> Optional[Dict[str, Any]]:
    """
    Fetches token data from the Uniswap subgraph.

    Args:
        token (str): The address of the token.

    Returns:
        Optional[Dict[str, Any]]: Token data if found, otherwise None.
    """
    try:
        fetcher = UniswapDataFetcher(RPC_URL, UNISWAP_SUBGRAPH_URL)
        token_data = fetcher.fetch_token_data(token)
        return token_data
    except Exception as e:
        logger.error("Failed to fetch token data: {}", e)
        return None


def fetch_pair_data(
    token0: str, token1: str
) -> Optional[Dict[str, Any]]:
    """
    Fetches pair data from the Uniswap subgraph.

    Args:
        token0 (str): The address of the first token in the pair.
        token1 (str): The address of the second token in the pair.

    Returns:
        Optional[Dict[str, Any]]: Pair data if found, otherwise None.
    """
    try:
        fetcher = UniswapDataFetcher(RPC_URL, UNISWAP_SUBGRAPH_URL)
        pair_data = fetcher.fetch_pair_data(token0, token1)
        return pair_data
    except Exception as e:
        logger.error("Failed to fetch pair data: {}", e)
        return None


def fetch_pool_volume(pool_address: str) -> Optional[float]:
    """
    Fetches the volume of a pool from the Uniswap subgraph.

    Args:
        pool_address (str): The address of the pool.

    Returns:
        Optional[float]: The volume of the pool if found, otherwise None.
    """
    try:
        fetcher = UniswapDataFetcher(RPC_URL, UNISWAP_SUBGRAPH_URL)
        pool_volume = fetcher.fetch_pool_volume(pool_address)
        return pool_volume
    except Exception as e:
        logger.error("Failed to fetch pool volume: {}", e)
        return None


def fetch_liquidity_positions(
    user_address: str,
) -> Optional[List[Dict[str, Any]]]:
    """
    Fetches the liquidity positions of a user from the Uniswap subgraph.

    Args:
        user_address (str): The address of the user.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of liquidity positions if found, otherwise None.
    """
    try:
        fetcher = UniswapDataFetcher(RPC_URL, UNISWAP_SUBGRAPH_URL)
        liquidity_positions = fetcher.fetch_liquidity_positions(
            user_address
        )
        return liquidity_positions
    except Exception as e:
        logger.error("Failed to fetch liquidity positions: {}", e)
        return None


def fetch_all_uniswap_data(
    token: str, pair: str, pool_address: str
) -> str:
    """
    Fetches all data for a given token, pair, and pool address.

    Args:
        token (str): The address of the token.
        pair (str): The pair of tokens.
        pool_address (str): The address of the pool.

    Returns:
        str: A formatted string containing the token data, pair data, and pool volume.
    """
    try:
        token_data = fetch_token_data(token)
        pair_data = fetch_pair_data(pair[0], pair[1])
        pool_volume = fetch_pool_volume(pool_address)
        formatted_data = f"Token Data: {token_data}\nPair Data: {pair_data}\nPool Volume: {pool_volume}"
        return formatted_data
    except Exception as e:
        logger.error("Failed to fetch all data: {}", e)
        return "Failed to fetch all data"


# # Example usage
# if __name__ == "__main__":
#     RPC_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
#     UNISWAP_SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"

#     fetcher = UniswapDataFetcher(RPC_URL, UNISWAP_SUBGRAPH_URL)

#     token_data = fetcher.fetch_token_data("0xdAC17F958D2ee523a2206206994597C13D831ec7")  # Example for USDT
#     logger.info("Token Data: {}", token_data)

#     pair_data = fetcher.fetch_pair_data(
#         "0xdAC17F958D2ee523a2206206994597C13D831ec7",
#         "0xC02aaA39b223FE8D0A0E5C4F27eAD9083C756Cc2"
#     )  # Example for USDT-WETH pair
#     logger.info("Pair Data: {}", pair_data)

#     pool_volume = fetcher.fetch_pool_volume("0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc")  # Example for USDT-WETH pool
#     logger.info("Pool Volume: {}", pool_volume)

#     liquidity_positions = fetcher.fetch_liquidity_positions("0xYourWalletAddress")
#     logger.info("Liquidity Positions: {}", liquidity_positions)
