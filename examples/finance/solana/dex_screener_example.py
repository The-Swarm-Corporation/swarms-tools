"""
Example usage of the DexScreener API client.

This example demonstrates how to use various endpoints of the DexScreener API
to fetch token information, search pairs, and handle responses.
"""

import asyncio
from loguru import logger

from swarms_tools.finance.dex_screener import DexScreenerAPI


async def main():
    # Initialize the API client
    dex_screener = DexScreenerAPI(timeout=30)

    try:
        # Example 1: Get latest token profiles
        logger.info("Fetching latest token profiles...")
        profiles = await dex_screener.get_latest_token_profiles()
        logger.info(f"Found {len(profiles)} token profiles")

        # Example 2: Search for a specific token pair
        search_query = "USDT"
        logger.info(
            f"Searching for pairs matching '{search_query}'..."
        )
        pairs = await dex_screener.search_pairs(search_query)

        # Print some information about the found pairs
        for pair in pairs[:3]:  # Show first 3 pairs
            logger.info(
                f"Found pair: {pair.base_token.symbol}/{pair.quote_token.symbol}"
            )
            logger.info(
                f"Price: ${pair.price_usd if pair.price_usd else 'N/A'}"
            )
            if pair.liquidity:
                logger.info(f"Liquidity: ${pair.liquidity.usd:,.2f}")
            logger.info("---")

        # Example 3: Get specific pair information
        # Using Ethereum USDT/WETH pair as an example
        chain_id = "ethereum"
        pair_id = "0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852"  # USDT-WETH pair

        logger.info(
            f"Fetching specific pair info for {chain_id}/{pair_id}..."
        )
        pair_info = await dex_screener.get_pair(chain_id, pair_id)

        if pair_info:
            logger.info("Pair Details:")
            logger.info(f"Base Token: {pair_info.base_token.symbol}")
            logger.info(
                f"Quote Token: {pair_info.quote_token.symbol}"
            )
            logger.info(
                f"Price (USD): ${pair_info.price_usd if pair_info.price_usd else 'N/A'}"
            )
            if pair_info.liquidity:
                logger.info(
                    f"Total Liquidity: ${pair_info.liquidity.usd:,.2f}"
                )

        # Example 4: Get token pairs for multiple addresses
        token_addresses = [
            "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
        ]

        logger.info("Fetching pairs for multiple tokens...")
        token_pairs = await dex_screener.get_token_pairs(
            chain_id, token_addresses
        )

        for pair in token_pairs[:3]:  # Show first 3 pairs
            logger.info(
                f"Token Pair: {pair.base_token.symbol}/{pair.quote_token.symbol}"
            )
            logger.info(f"DEX: {pair.dex_id}")
            logger.info(f"URL: {pair.url}")
            logger.info("---")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    finally:
        # Cleanup
        del dex_screener


if __name__ == "__main__":
    # Set up logging
    logger.add("dex_screener_example.log", rotation="500 MB")

    # Run the async example
    asyncio.run(main())
