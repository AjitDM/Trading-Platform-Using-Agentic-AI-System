from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.graphs.trading_graph import start_trading_run

router = APIRouter()


class TradingRunRequest(BaseModel):
    symbol: str = Field(
        examples=["TCS.NS"],
        min_length=1,
    )


@router.post("/run")
def run_trading_workflow(request: TradingRunRequest) -> dict:
    try:
        return start_trading_run(request.symbol)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc