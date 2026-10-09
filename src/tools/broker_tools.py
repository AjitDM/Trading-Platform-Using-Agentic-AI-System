from langchain_core.tools import tool

from src.brokers.factory import get_broker
from src.schemas.orders import OrderRequest


@tool
def submit_order(
    symbol: str,
    side: str,
    quantity: int,
    order_type: str = "MARKET",
) -> dict:
    """
    Submit an order through the configured broker.

    This tool must never be exposed to an unconstrained LLM agent in production.
    The graph risk node and human approval node must run first.
    """
    order = OrderRequest(
        symbol=symbol,
        side=side.upper(),
        quantity=quantity,
        order_type=order_type.upper(),
    )
    return get_broker().place_order(order)