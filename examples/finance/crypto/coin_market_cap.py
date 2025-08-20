from loguru import logger
from swarms_tools.finance.coin_market_cap import (
    coinmarketcap_api,
)

if __name__ == "__main__":
    # Set up logging
    logger.add(
        "coinmarketcap_api.log", rotation="500 MB", level="INFO"
    )

    # Example usage
    single_coin = coinmarketcap_api(["Bitcoin"])
    print("Single Coin Data:", single_coin)

    multiple_coins = coinmarketcap_api(
        ["Bitcoin", "Ethereum", "Tether"]
    )
    print("Multiple Coins Data:", multiple_coins)

    all_coins = coinmarketcap_api()
    print("All Coins Data:", all_coins)
