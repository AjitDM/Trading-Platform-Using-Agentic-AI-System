from langgraph.types import interrupt

from src.config.settings import get_settings
from src.states.state import TradingState


def approval_node(state: TradingState) -> dict:
    settings = get_settings()

    if not settings.require_human_approval:
        return {"approval_status": "approved"}

    response = interrupt(
        {
            "type": "trade_approval",
            "run_id": state["run_id"],
            "message": "Approve the proposed order?",
            "signal": state["signal"].model_dump(),
            "order": state["order"].model_dump(),
        }
    )

    approved = bool(response.get("approved", False))

    return {
        "approval_status": "approved" if approved else "rejected",
    }