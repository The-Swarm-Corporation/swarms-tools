from typing import Any
import httpx

# json import removed - using orjson instead
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("defillama-mcp")

# Constants
DEFI_API_BASE = "https://api.llama.fi"
COIN_API_BASE = "https://coins.llama.fi"
USER_AGENT = "DEFI-APP/1.0"


@mcp.tool()
async def get_protocols() -> dict[Any, Any]:
    """Get all protocols from defillama.

    Args:
    """
    url = f"{DEFI_API_BASE}/protocols"
    data = await make_request(url)

    return data[:20]


@mcp.tool()
async def get_protocol_tvl(protocol: str) -> dict[Any, Any]:
    """Get a defi protocol tvl from defillama
    Args:
        protocol: protocol name
    """
    url = f"{DEFI_API_BASE}/protocol/{protocol}"
    data = await make_request(url)
    return data["currentChainTvls"]


@mcp.tool()
async def get_chain_tvl(chain: str) -> dict[Any, Any]:
    """Get a chain's tvl

    Args:
        chain: chain name
    """
    url = f"{DEFI_API_BASE}/v2/historicalChainTvl/{chain}"
    data = await make_request(url)
    return data[:30]


@mcp.tool()
async def get_token_prices(token: str) -> dict[Any, Any]:
    """Get a token's price
    Args:
        token: token name
    """
    url = f"{COIN_API_BASE}/prices/current/{token}"
    data = await make_request(url)
    return data


async def make_request(url: str) -> dict[str, Any] | None:
    """Make a request to the API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url, headers=headers, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


# if __name__ == "__main__":
#     mcp.run(transport="stdio")
