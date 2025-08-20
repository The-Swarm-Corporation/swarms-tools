from loguru import logger
from swarms_tools.finance.yahoo_finance import (
    yahoo_finance_api,
)

if __name__ == "__main__":
    # Set up logging
    logger.add(
        "yahoo_finance_api.log", rotation="500 MB", level="INFO"
    )

    # Example usage
    single_stock = yahoo_finance_api(
        ["AAPL"]
    )  # Fetch data for a single stock
    print("Single Stock Data:", single_stock)

    # multiple_stocks = yahoo_finance_api(
    #     ["AAPL", "GOOG", "MSFT"]
    # )  # Fetch data for multiple stocks
    # print("Multiple Stocks Data:", multiple_stocks)
