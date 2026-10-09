from src.data.market_data import MarketDataService
from src.data.news_data import NewsDataService
from src.states.state import TradingState


def market_data_node(state: TradingState) -> dict:
    try:
        market = MarketDataService().get_snapshot(state["symbol"])
        market.news = NewsDataService().get_news(state["symbol"])

        return {"market": market}
    except Exception as exc:
        return {"errors": [f"Market data retrieval failed: {exc}"]}