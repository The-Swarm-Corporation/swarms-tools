import os
from typing import Optional, Tuple

from ib_insync import IB, Stock, MarketOrder, LimitOrder, Order
from dotenv import load_dotenv
from loguru import logger
import yfinance as yf

# Load environment variables from a .env file
load_dotenv()

# Retrieve connection parameters from environment variables
IB_HOST: str = os.getenv("IB_HOST", "127.0.0.1")
IB_PORT: int = int(os.getenv("IB_PORT", "7497"))
CLIENT_ID: int = int(os.getenv("CLIENT_ID", "1"))


def connect_ib() -> IB:
    """
    Establish a connection to Interactive Brokers TWS/IB Gateway using parameters from the .env file.

    Returns
    -------
    IB
        A connected instance of the IB class.
    """
    ib = IB()
    logger.info(
        "Connecting to IB at {}:{} with clientId {}",
        IB_HOST,
        IB_PORT,
        CLIENT_ID,
    )
    ib.connect(IB_HOST, IB_PORT, clientId=CLIENT_ID)
    logger.info("Connected to IB")
    return ib


def calculate_position_size(
    stock: str, risk_capital: float, stop_loss_price: float
) -> Tuple[str, float, int]:
    """
    Calculates the position size for a given stock based on your risk capital and stop loss price.

    The function uses Yahoo Finance to fetch the current stock price and name. It then calculates
    the risk per share as the absolute difference between the current price and the stop loss price.
    The order size is determined by dividing the risk capital by the risk per share.

    Parameters
    ----------
    stock : str
        The ticker symbol of the stock (e.g., 'AAPL').
    risk_capital : float
        The maximum dollar amount you are willing to risk on the trade.
    stop_loss_price : float
        The stop loss price for the trade.

    Returns
    -------
    Tuple[str, float, int]
        A tuple containing:
            - The stock's name (if available; otherwise, the ticker symbol),
            - The current price of the stock,
            - The calculated order size (number of shares to buy).

    Raises
    ------
    ValueError
        If the current price cannot be determined or if risk per share is zero.
    """
    logger.info("Fetching data for stock: {}", stock)
    ticker = yf.Ticker(stock)
    info = ticker.info

    stock_name = info.get("shortName", stock)
    current_price = info.get("regularMarketPrice")

    if current_price is None:
        raise ValueError(
            f"Could not retrieve current price for {stock}"
        )

    # Calculate risk per share (make sure it's positive)
    risk_per_share = abs(current_price - stop_loss_price)
    if risk_per_share <= 0:
        raise ValueError(
            "Risk per share must be positive. Check the current price and stop loss price."
        )

    # Calculate the order size (number of shares)
    order_size = int(risk_capital / risk_per_share)
    logger.info(
        "Calculated position size for {}: Stock Name: {}, Current Price: {}, Order Size: {}",
        stock,
        stock_name,
        current_price,
        order_size,
    )
    return stock_name, current_price, order_size


def place_buy_with_bracket(
    stock: str,
    quantity: int,
    take_profit_price: float,
    stop_loss_price: float,
    ib: Optional[IB] = None,
) -> None:
    """
    Places a market buy order for the given stock with attached bracket orders:
      - A limit sell order for taking profit.
      - A stop order for limiting losses.

    Parameters
    ----------
    stock : str
        The ticker symbol of the stock (e.g., 'AAPL').
    quantity : int
        The number of shares to buy.
    take_profit_price : float
        The price at which to take profit by selling.
    stop_loss_price : float
        The price at which to stop loss by selling.
    ib : IB, optional
        An instance of IB. If None, a new connection will be established using .env settings.

    Returns
    -------
    None
    """
    if ib is None:
        ib = connect_ib()

    # Create the contract for the stock.
    contract = Stock(stock, "SMART", "USD")
    logger.info(
        "Placing buy order with bracket orders for stock: {}", stock
    )

    # Parent market order to buy the stock.
    parent_order = MarketOrder("BUY", quantity)
    parent_order.transmit = (
        False  # Hold transmission to attach child orders.
    )
    ib.placeOrder(contract, parent_order)

    # Take profit order (limit sell).
    take_profit_order = LimitOrder(
        "SELL", quantity, take_profit_price
    )
    take_profit_order.parentId = parent_order.orderId
    take_profit_order.transmit = False

    # Stop loss order (stop sell order).
    stop_loss_order = Order()
    stop_loss_order.action = "SELL"
    stop_loss_order.totalQuantity = quantity
    stop_loss_order.orderType = "STP"
    stop_loss_order.auxPrice = stop_loss_price
    stop_loss_order.parentId = parent_order.orderId
    stop_loss_order.transmit = (
        True  # Final child order transmits entire bracket
    )

    # Place child orders.
    ib.placeOrder(contract, take_profit_order)
    ib.placeOrder(contract, stop_loss_order)

    # Now transmit the parent order along with its children.
    parent_order.transmit = True

    logger.info(
        "Submitted bracket orders for {}. Parent Order ID: {}. Take Profit at: {}, Stop Loss at: {}",
        stock,
        parent_order.orderId,
        take_profit_price,
        stop_loss_price,
    )


def place_sell_order(
    stock: str,
    quantity: int,
    price: Optional[float] = None,
    ib: Optional[IB] = None,
) -> None:
    """
    Places a sell order for the given stock. If a price is specified, a limit order is used;
    otherwise, a market order is submitted.

    Parameters
    ----------
    stock : str
        The ticker symbol of the stock (e.g., 'AAPL').
    quantity : int
        The number of shares to sell.
    price : float, optional
        The limit price at which to sell. If None, a market order is placed.
    ib : IB, optional
        An instance of IB. If None, a new connection will be established using .env settings.

    Returns
    -------
    None
    """
    if ib is None:
        ib = connect_ib()

    # Create the contract for the stock.
    contract = Stock(stock, "SMART", "USD")
    if price is not None:
        logger.info(
            "Placing limit sell order for {} at price {}",
            stock,
            price,
        )
        order = LimitOrder("SELL", quantity, price)
    else:
        logger.info("Placing market sell order for {}", stock)
        order = MarketOrder("SELL", quantity)

    ib.placeOrder(contract, order)
    logger.info(
        "Sell order submitted for {}. Order ID: {}",
        stock,
        order.orderId,
    )


# # Example usage:
# if __name__ == "__main__":
#     # Connect to IB using .env variables.
#     ib_connection = connect_ib()

#     # Example: Calculate position size for 'AAPL' with a risk capital of $100 and a stop loss at $165.
#     try:
#         stock_name, current_price, order_size = calculate_position_size(
#             stock="AAPL",
#             risk_capital=100.0,
#             stop_loss_price=165.0
#         )
#         logger.info("Stock: {} | Current Price: {} | Order Size: {}", stock_name, current_price, order_size)
#     except Exception as e:
#         logger.error("Error calculating position size: {}", e)

#     # Example: Place a buy order with bracket orders for 'AAPL'
#     place_buy_with_bracket(
#         stock="AAPL",
#         quantity=order_size if order_size > 0 else 1,
#         take_profit_price=175.0,
#         stop_loss_price=165.0,
#         ib=ib_connection
#     )

#     # Example: Place a market sell order for 'AAPL'
#     place_sell_order(
#         stock="AAPL",
#         quantity=order_size if order_size > 0 else 1,
#         ib=ib_connection
#     )

#     # Keep the event loop running to listen for updates.
#     ib_connection.run()
