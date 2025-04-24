import asyncio
from swarms_tools.finance.defillama_mcp_tools import (
    get_protocols,
    get_protocol_tvl,
    get_chain_tvl,
    get_token_prices,
)


async def main():
    print("Fetching protocols...")
    protocols = await get_protocols()

    print("\nFetching protocol TVL for uniswap-v3...")
    protocol_tvl = await get_protocol_tvl("uniswap-v3")
    print(protocol_tvl)

    print("\nFetching chain TVL for Ethereum...")
    chain_tvl = await get_chain_tvl("Ethereum")
    print(chain_tvl)

    print("\nFetching token prices for Bitcoin...")
    token_prices = await get_token_prices("coingecko:bitcoin")
    print(token_prices)


if __name__ == "__main__":
    asyncio.run(main())
    