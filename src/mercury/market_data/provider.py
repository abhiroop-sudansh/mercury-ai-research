from datetime import date, timedelta

import pandas as pd
import yfinance as yf


class MarketDataError(Exception):
    """Raised when market data cannot be retrieved or validated."""


def download_prices(
    symbol: str,
    event_date: date,
    days_before: int = 10,
    days_after: int = 15,
) -> pd.DataFrame:
    normalized_symbol = symbol.strip().upper()

    start_date = event_date - timedelta(days=days_before)
    end_date = event_date + timedelta(days=days_after)

    prices = yf.download(
        normalized_symbol,
        start=start_date.isoformat(),
        end=end_date.isoformat(),
        auto_adjust=True,
        progress=False,
    )

    if prices.empty:
        raise MarketDataError(
            f"No market data found for symbol {normalized_symbol}"
        )

    prices = prices.reset_index()

    if isinstance(prices.columns, pd.MultiIndex):
        prices.columns = [
            column[0] if isinstance(column, tuple) else column
            for column in prices.columns
        ]

    required_columns = {"Date", "Close"}

    if not required_columns.issubset(prices.columns):
        raise MarketDataError(
            f"Missing required columns: {sorted(required_columns)}"
        )

    prices["Date"] = pd.to_datetime(prices["Date"]).dt.date
    prices = prices.sort_values("Date").reset_index(drop=True)

    return prices[["Date", "Close"]]