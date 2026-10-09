import operator
from typing import Annotated, Any, TypedDict

from src.schemas.analysis import AnalysisBundle
from src.schemas.market import MarketSnapshot
from src.schemas.orders import OrderRequest
from src.schemas.portfolio import PortfolioSnapshot
from src.schemas.signals import TradingSignal


class TradingState(TypedDict, total=False):
    run_id: str
    symbol: str
    timeframe: str

    market: MarketSnapshot
    portfolio: PortfolioSnapshot
    analysis: AnalysisBundle
    signal: TradingSignal
    order: OrderRequest

    risk_passed: bool
    approval_required: bool
    approval_status: str
    execution_result: dict[str, Any]
    audit_record_id: int | None

    messages: Annotated[list[Any], operator.add]
    errors: Annotated[list[str], operator.add]