from pydantic import BaseModel, Field


class Position(BaseModel):
    symbol: str
    quantity: int
    average_price: float = Field(gt=0)
    last_price: float = Field(gt=0)
    unrealized_pnl: float


class PortfolioSnapshot(BaseModel):
    total_value: float = Field(ge=0)
    available_cash: float = Field(ge=0)
    daily_pnl: float
    drawdown_percent: float = Field(ge=0)
    positions: list[Position] = Field(default_factory=list)