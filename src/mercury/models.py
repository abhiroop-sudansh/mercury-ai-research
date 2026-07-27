from datetime import date

from pydantic import BaseModel, Field


class EventAnalysisRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=10)
    event_date: date
    benchmark: str = Field(default="SPY", min_length=1, max_length=10)


class EventAnalysisResult(BaseModel):
    symbol: str
    event_date: date
    benchmark: str
    return_0_1: float
    return_0_5: float
    benchmark_return_0_1: float
    market_adjusted_return_0_1: float
    status: str