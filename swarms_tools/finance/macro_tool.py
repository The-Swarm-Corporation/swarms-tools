import httpx
import yfinance as yf


def fetch_macro_financial_data():
    """
    Fetches real-time macroeconomic and financial data including gold, S&P 500, and more from various sources.

    Returns:
        str: A string containing the financial data.
    """
    try:
        # Define tickers for gold, S&P 500, and other variables
        tickers = {
            "Gold": "GC=F",
            "S&P 500": "^GSPC",
            "NASDAQ": "^IXIC",
            "DXY (Dollar Index)": "DX-Y.NYB",
            "Brent Crude": "BZ=F",
        }

        # Initialize a dictionary to store results
        data = {}

        # Fetch data from Yahoo Finance
        for ticker, symbol in tickers.items():
            try:
                ticker_obj = yf.Ticker(symbol)
                history = ticker_obj.history(period="1d")
                price = (
                    history["Close"].iloc[-1]
                    if not history.empty
                    else "N/A"
                )
                data[ticker] = price
            except Exception as inner_error:
                data[ticker] = f"Error fetching data: {inner_error}"

        # Fetch additional data from other APIs
        try:
            # Example: Fetching exchange rates from a public API
            exchange_rate_url = (
                "https://api.exchangerate-api.com/v4/latest/USD"
            )
            response = httpx.get(exchange_rate_url)
            response.raise_for_status()
            exchange_data = response.json()
            data["EUR/USD Exchange Rate"] = exchange_data.get(
                "rates", {}
            ).get("EUR", "N/A")
            data["GBP/USD Exchange Rate"] = exchange_data.get(
                "rates", {}
            ).get("GBP", "N/A")
        except Exception as ex:
            data["Exchange Rates"] = (
                f"Error fetching exchange rates: {ex}"
            )

        # Format the output as a string
        result = "\n".join(
            [f"{key}: {value}" for key, value in data.items()]
        )
        return result

    except Exception as e:
        return f"Error fetching data: {e}"


# print(fetch_macro_financial_data())
