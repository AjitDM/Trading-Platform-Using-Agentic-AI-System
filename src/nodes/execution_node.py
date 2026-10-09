from src.brokers.factory import get_broker
from src.states.state import TradingState


def execution_node(state: TradingState) -> dict:
    if not state.get("risk_passed"):
        return {
            "execution_result": {
                "status": "SKIPPED",
                "reason": "Risk validation did not pass.",
            }
        }

    if state.get("approval_status") != "approved":
        return {
            "execution_result": {
                "status": "SKIPPED",
                "reason": "Trade was not approved.",
            }
        }

    try:
        result = get_broker().place_order(state["order"])
        return {"execution_result": result}
    except Exception as exc:
        return {
            "execution_result": {
                "status": "FAILED",
                "reason": str(exc),
            },
            "errors": [f"Order execution failed: {exc}"],
        }