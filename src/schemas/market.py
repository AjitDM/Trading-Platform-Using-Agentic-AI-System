from datetime import datetime

from pydantic import BaseModel, Field


class OHLCV(BaseModel):
    timestamp: datetime
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    volume: float = Field(ge=0)


class MarketSnapshot(BaseModel):
    symbol: str
    exchange: str = "NSE"
    currency: str = "INR"
    last_price: float = Field(gt=0)
    candles: list[OHLCV] = Field(default_factory=list)
    indicators: dict[str, float] = Field(default_factory=dict)
    news: list[dict] = Field(default_factory=list)
    fetched_at: datetime