"""
Sector Analysis Module

This module provides functionality to analyze GICS sector ETFs using RSI (Relative Strength Index)
to identify overbought and oversold sectors, followed by detailed industry group analysis.

Main features:
- Fetch sector ETF data using yfinance
- Calculate RSI values for sector ETFs using pandas
- Identify strongest and weakest sectors
- Analyze industry groups within extreme sectors
"""

from typing import Dict, List, Tuple

import pandas as pd
import yfinance as yf
from loguru import logger


def calculate_rsi(data: pd.Series, periods: int = 14) -> pd.Series:
    """
    Calculate RSI using pandas operations.

    Args:
        data (pd.Series): Price series data
        periods (int): RSI calculation window

    Returns:
        pd.Series: RSI values
    """
    # Calculate price changes
    delta = data.diff()

    # Separate gains and losses
    gains = delta.copy()
    losses = delta.copy()
    gains[gains < 0] = 0
    losses[losses > 0] = 0
    losses = abs(losses)

    # Calculate rolling averages
    avg_gain = gains.rolling(window=periods).mean()
    avg_loss = losses.rolling(window=periods).mean()

    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


class SectorAnalyzer:
    """Class for analyzing sector ETFs and their industry groups using RSI."""

    # GICS Sector ETFs mapping
    SECTOR_ETFS = {
        "XLE": "Energy",
        "XLF": "Financials",
        "XLK": "Technology",
        "XLV": "Healthcare",
        "XLI": "Industrials",
        "XLP": "Consumer Staples",
        "XLY": "Consumer Discretionary",
        "XLB": "Materials",
        "XLU": "Utilities",
        "XLRE": "Real Estate",
        "XLC": "Communication Services",
    }

    def __init__(self, period: str = "1y", rsi_window: int = 14):
        """
        Initialize SectorAnalyzer.

        Args:
            period (str): Time period for data analysis (default: "1y")
            rsi_window (int): RSI calculation window (default: 14)
        """
        self.period = period
        self.rsi_window = rsi_window
        logger.info(
            f"Initialized SectorAnalyzer with period={period}, rsi_window={rsi_window}"
        )

    def fetch_sector_data(self) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical data for all sector ETFs.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary mapping ETF symbols to their historical data
        """
        sector_data = {}
        for symbol in self.SECTOR_ETFS.keys():
            try:
                logger.info(f"Fetching data for {symbol}")
                etf = yf.Ticker(symbol)
                sector_data[symbol] = etf.history(period=self.period)
            except Exception as e:
                logger.error(
                    f"Error fetching data for {symbol}: {str(e)}"
                )
        return sector_data

    def calculate_sector_rsi(
        self, sector_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, float]:
        """
        Calculate current RSI values for all sectors using pandas implementation.

        Args:
            sector_data (Dict[str, pd.DataFrame]): Historical sector data

        Returns:
            Dict[str, float]: Dictionary mapping sector symbols to their RSI values
        """
        rsi_values = {}
        for symbol, data in sector_data.items():
            try:
                rsi = calculate_rsi(data["Close"], self.rsi_window)
                current_rsi = rsi.iloc[-1]
                rsi_values[symbol] = current_rsi
                logger.debug(f"RSI for {symbol}: {current_rsi:.2f}")
            except Exception as e:
                logger.error(
                    f"Error calculating RSI for {symbol}: {str(e)}"
                )
        return rsi_values

    def identify_extreme_sectors(
        self,
        rsi_values: Dict[str, float],
        overbought_threshold: float = 70,
        oversold_threshold: float = 30,
    ) -> Tuple[List[str], List[str]]:
        """
        Identify sectors with extreme RSI values.

        Args:
            rsi_values (Dict[str, float]): Dictionary of sector RSI values
            overbought_threshold (float): RSI threshold for overbought condition
            oversold_threshold (float): RSI threshold for oversold condition

        Returns:
            Tuple[List[str], List[str]]: Lists of overbought and oversold sectors
        """
        overbought = [
            symbol
            for symbol, rsi in rsi_values.items()
            if rsi >= overbought_threshold
        ]
        oversold = [
            symbol
            for symbol, rsi in rsi_values.items()
            if rsi <= oversold_threshold
        ]

        logger.info(f"Overbought sectors: {overbought}")
        logger.info(f"Oversold sectors: {oversold}")

        return overbought, oversold

    def analyze_sectors(self) -> Dict[str, any]:
        """
        Perform complete sector analysis.

        Returns:
            Dict[str, any]: Analysis results including RSI values and extreme sectors
        """
        try:
            logger.info("Starting sector analysis")

            # Fetch data and calculate RSIs
            sector_data = self.fetch_sector_data()
            rsi_values = self.calculate_sector_rsi(sector_data)

            # Identify extreme sectors
            overbought, oversold = self.identify_extreme_sectors(
                rsi_values
            )

            results = {
                "rsi_values": rsi_values,
                "overbought_sectors": overbought,
                "oversold_sectors": oversold,
                "timestamp": pd.Timestamp.now(),
            }

            logger.success("Sector analysis completed successfully")
            return results

        except Exception as e:
            logger.error(f"Error in sector analysis: {str(e)}")
            raise


# def analyze_index_sectors():
#     """Main function for demonstration purposes."""
#     analyzer = SectorAnalyzer()
#     results = analyzer.analyze_sectors()

#     # Print results
#     print("\nSector RSI Analysis Results:")
#     print("-" * 40)
#     for symbol, rsi in results["rsi_values"].items():
#         sector_name = SectorAnalyzer.SECTOR_ETFS[symbol]
#         print(f"{sector_name} ({symbol}): RSI = {rsi:.2f}")

#     print("\nExtreme Sectors:")
#     print(
#         "Overbought:",
#         ", ".join(results["overbought_sectors"]) or "None",
#     )
#     print(
#         "Oversold:", ", ".join(results["oversold_sectors"]) or "None"
#     )


# if __name__ == "__main__":
#     analyze_index_sectors()
