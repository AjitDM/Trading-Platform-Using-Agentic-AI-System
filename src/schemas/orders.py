from typing import Literal

from pydantic import BaseModel, Field, model_validator


class OrderRequest(BaseModel):
    symbol: str
    exchange: str = "NSE"
    side: Literal["BUY", "SELL"]
    order_type: Literal["MARKET", "LIMIT", "SL", "SL-M"] = "MARKET"
    quantity: int = Field(gt=0)
    price: float | None = Field(default=None, gt=0)
    trigger_price: float | None = Field(default=None, gt=0)
    product: Literal["CNC", "MIS"] = "CNC"
    tag: str = "agentic-trading"

    @model_validator(mode="after")
    def validate_limit_price(self) -> "OrderRequest":
        if self.order_type == "LIMIT" and self.price is None:
            raise ValueError("A LIMIT order requires price.")
        return self