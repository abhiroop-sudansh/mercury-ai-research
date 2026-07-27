from datetime import date

import pandas as pd


class EventDateError(Exception):
    """Raised when an event cannot be matched to a trading date."""


def find_event_row(prices: pd.DataFrame, event_date: date) -> int:
    matching_rows = prices.index[prices["Date"] >= event_date].tolist()

    if not matching_rows:
        raise EventDateError(
            f"No trading date found on or after {event_date}"
        )

    return matching_rows[0]


def calculate_window_return(
    prices: pd.DataFrame,
    start_index: int,
    trading_days_after: int,
) -> float:
    end_index = start_index + trading_days_after

    if end_index >= len(prices):
        raise EventDateError(
            "Insufficient price history for the requested return window"
        )

    start_price = float(prices.iloc[start_index]["Close"])
    end_price = float(prices.iloc[end_index]["Close"])

    if start_price <= 0:
        raise ValueError("Starting price must be greater than zero")

    return (end_price - start_price) / start_price