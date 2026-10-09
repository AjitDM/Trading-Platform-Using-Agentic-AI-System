from src.risk.validators import RiskViolation, validate_order
from src.states.state import TradingState


def risk_node(state: TradingState) -> dict:
    signal = state.get("signal")
    order = state.get("order")
    market = state.get("market")
    portfolio = state.get("portfolio")

    if signal is None or signal.action == "hold" or order is None:
        return {
            "risk_passed": False,
            "approval_required": False,
        }

    if market is None or portfolio is None:
        return {
            "risk_passed": False,
            "approval_required": False,
            "errors": ["Risk validation failed: market or portfolio missing."],
        }

    try:
        validate_order(
            order=order,
            portfolio=portfolio,
            current_price=market.last_price,
        )

        return {
            "risk_passed": True,
            "approval_required": True,
        }
    except RiskViolation as exc:
        return {
            "risk_passed": False,
            "approval_required": False,
            "errors": [f"Risk validation rejected order: {exc}"],
        }