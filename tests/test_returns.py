from datetime import date

import pandas as pd
import pytest

from mercury.analytics.returns import (
    calculate_window_return,
    find_event_row,
)


@pytest.fixture
def sample_prices() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Date": [
                date(2026, 1, 5),
                date(2026, 1, 6),
                date(2026, 1, 7),
                date(2026, 1, 8),
                date(2026, 1, 9),
                date(2026, 1, 12),
            ],
            "Close": [
                100.0,
                102.0,
                101.0,
                105.0,
                108.0,
                110.0,
            ],
        }
    )


def test_find_event_row_exact_date(
    sample_prices: pd.DataFrame,
) -> None:
    row = find_event_row(
        sample_prices,
        date(2026, 1, 6),
    )

    assert row == 1


def test_find_event_row_weekend_uses_next_trading_day(
    sample_prices: pd.DataFrame,
) -> None:
    row = find_event_row(
        sample_prices,
        date(2026, 1, 10),
    )

    assert row == 5


def test_calculate_one_day_return(
    sample_prices: pd.DataFrame,
) -> None:
    result = calculate_window_return(
        sample_prices,
        start_index=0,
        trading_days_after=1,
    )

    assert result == pytest.approx(0.02)


def test_calculate_five_day_return(
    sample_prices: pd.DataFrame,
) -> None:
    result = calculate_window_return(
        sample_prices,
        start_index=0,
        trading_days_after=5,
    )

    assert result == pytest.approx(0.10)