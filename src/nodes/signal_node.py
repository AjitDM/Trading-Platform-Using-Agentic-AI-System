from src.config.settings import get_settings
from src.risk.position_sizing import calculate_fixed_fraction_quantity
from src.schemas.orders import OrderRequest
from src.schemas.signals import TradingSignal
from src.states.state import TradingState


def signal_node(state: TradingState) -> dict:
    settings = get_settings()
    market = state.get("market")
    portfolio = state.get("portfolio")
    consensus = state.get("analysis").consensus if state.get("analysis") else None

    if market is None or portfolio is None or consensus is None:
        return {
            "signal": TradingSignal(
                symbol=state["symbol"],
                action="hold",
                confidence=0.0,
                quantity=0,
                rationale="Required market, portfolio, or consensus information is missing.",
            )
        }

    if consensus.confidence < settings.min_signal_confidence:
        return {
            "signal": TradingSignal(
                symbol=state["symbol"],
                action="hold",
                confidence=consensus.confidence,
                quantity=0,
                rationale=(
                    f"Consensus confidence {consensus.confidence:.2f} is below "
                    f"the minimum threshold {settings.min_signal_confidence:.2f}."
                ),
                invalidation_conditions=consensus.risks,
            )
        }

    action_map = {
        "bullish": "buy",
        "bearish": "sell",
        "neutral": "hold",
    }
    action = action_map[consensus.direction]

    if action == "hold":
        return {
            "signal": TradingSignal(
                symbol=state["symbol"],
                action="hold",
                confidence=consensus.confidence,
                quantity=0,
                rationale=consensus.thesis,
                invalidation_conditions=consensus.risks,
            )
        }

    quantity = calculate_fixed_fraction_quantity(
        portfolio_value=portfolio.total_value,
        entry_price=market.last_price,
        max_position_percent=settings.max_position_percent,
        max_order_value=settings.max_order_value,
    )

    if quantity == 0:
        return {
            "signal": TradingSignal(
                symbol=state["symbol"],
                action="hold",
                confidence=consensus.confidence,
                quantity=0,
                rationale="Risk sizing produced zero quantity.",
                invalidation_conditions=consensus.risks,
            )
        }

    stop_loss = (
        market.last_price * 0.98 if action == "buy" else market.last_price * 1.02
    )
    target_price = (
        market.last_price * 1.04 if action == "buy" else market.last_price * 0.96
    )

    signal = TradingSignal(
        symbol=state["symbol"],
        action=action,
        confidence=consensus.confidence,
        entry_price=market.last_price,
        stop_loss=round(stop_loss, 2),
        target_price=round(target_price, 2),
        quantity=quantity,
        rationale=consensus.thesis,
        invalidation_conditions=consensus.risks,
    )

    order = OrderRequest(
        symbol=state["symbol"],
        exchange=settings.exchange,
        side="BUY" if action == "buy" else "SELL",
        quantity=quantity,
        order_type="MARKET",
        product="CNC",
    )

    return {
        "signal": signal,
        "order": order,
    }