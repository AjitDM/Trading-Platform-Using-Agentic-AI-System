from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.graphs.trading_graph import start_trading_run

router = APIRouter()


class AnalysisRequest(BaseModel):
    symbol: str = Field(
        examples=["RELIANCE.NS"],
        min_length=1,
    )
    timeframe: str = "1d"


@router.post("/")
def analyze(request: AnalysisRequest) -> dict:
    try:
        return start_trading_run(
            symbol=request.symbol,
            timeframe=request.timeframe,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc