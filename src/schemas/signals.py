from typing import Literal

from pydantic import BaseModel, Field


class TradingSignal(BaseModel):
    symbol: str
    action: Literal["buy", "sell", "hold"]
    confidence: float = Field(ge=0, le=1)
    entry_price: float | None = Field(default=None, gt=0)
    stop_loss: float | None = Field(default=None, gt=0)
    target_price: float | None = Field(default=None, gt=0)
    quantity: int = Field(default=0, ge=0)
    rationale: str
    invalidation_conditions: list[str] = Field(default_factory=list)