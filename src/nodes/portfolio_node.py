from src.brokers.factory import get_broker
from src.states.state import TradingState


def portfolio_node(state: TradingState) -> dict:
    try:
        portfolio = get_broker().get_portfolio()
        return {"portfolio": portfolio}
    except Exception as exc:
        return {"errors": [f"Portfolio retrieval failed: {exc}"]}