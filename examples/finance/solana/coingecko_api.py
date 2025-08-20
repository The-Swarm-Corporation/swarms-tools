from swarms_tools.finance.coingecko_tool import (
    coin_gecko_coin_api,
)

if __name__ == "__main__":
    # Example: Fetch data for Bitcoin
    print(coin_gecko_coin_api("bitcoin"))
