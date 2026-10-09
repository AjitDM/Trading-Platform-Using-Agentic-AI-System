from langchain_core.tools import tool

from src.data.market_data import MarketDataService


@tool
def get_market_snapshot(symbol: str) -> dict:
    """Fetch recent daily OHLCV prices and deterministic technical indicators."""
    snapshot = MarketDataService().get_snapshot(symbol)
    return snapshot.model_dump(mode="json")