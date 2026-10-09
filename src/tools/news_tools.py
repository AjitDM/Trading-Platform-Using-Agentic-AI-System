from langchain_core.tools import tool

from src.data.news_data import NewsDataService


@tool
def get_company_news(symbol: str) -> list[dict]:
    """Fetch configured news records for a stock symbol."""
    return NewsDataService().get_news(symbol)