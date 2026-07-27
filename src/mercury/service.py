from mercury.analytics.returns import (
    calculate_window_return,
    find_event_row,
)
from mercury.market_data.provider import download_prices
from mercury.models import EventAnalysisRequest, EventAnalysisResult


def analyze_market_event(
    request: EventAnalysisRequest,
) -> EventAnalysisResult:
    symbol = request.symbol.strip().upper()
    benchmark = request.benchmark.strip().upper()

    stock_prices = download_prices(
        symbol=symbol,
        event_date=request.event_date,
    )

    benchmark_prices = download_prices(
        symbol=benchmark,
        event_date=request.event_date,
    )

    stock_event_index = find_event_row(
        stock_prices,
        request.event_date,
    )

    benchmark_event_index = find_event_row(
        benchmark_prices,
        request.event_date,
    )

    stock_return_0_1 = calculate_window_return(
        stock_prices,
        stock_event_index,
        trading_days_after=1,
    )

    stock_return_0_5 = calculate_window_return(
        stock_prices,
        stock_event_index,
        trading_days_after=5,
    )

    benchmark_return_0_1 = calculate_window_return(
        benchmark_prices,
        benchmark_event_index,
        trading_days_after=1,
    )

    market_adjusted_return = (
        stock_return_0_1 - benchmark_return_0_1
    )

    return EventAnalysisResult(
        symbol=symbol,
        event_date=request.event_date,
        benchmark=benchmark,
        return_0_1=stock_return_0_1,
        return_0_5=stock_return_0_5,
        benchmark_return_0_1=benchmark_return_0_1,
        market_adjusted_return_0_1=market_adjusted_return,
        status="success",
    )