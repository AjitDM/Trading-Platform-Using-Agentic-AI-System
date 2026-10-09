from langchain_core.tools import tool

from src.brokers.factory import get_broker


@tool
def get_portfolio_snapshot() -> dict:
    """Get the portfolio snapshot from the selected broker adapter."""
    return get_broker().get_portfolio().model_dump()