from src.risk.limits import get_risk_limits
from src.schemas.orders import OrderRequest
from src.schemas.portfolio import PortfolioSnapshot


class RiskViolation(Exception):
    pass


def validate_order(
    order: OrderRequest,
    portfolio: PortfolioSnapshot,
    current_price: float,
) -> None:
    limits = get_risk_limits()

    estimated_order_value = order.quantity * current_price
    max_position_value = portfolio.total_value * limits.max_position_percent / 100

    if order.quantity <= 0:
        raise RiskViolation("Order quantity must be positive.")

    if estimated_order_value > limits.max_order_value:
        raise RiskViolation(
            f"Order value {estimated_order_value:.2f} exceeds maximum order value "
            f"{limits.max_order_value:.2f}."
        )

    if estimated_order_value > max_position_value:
        raise RiskViolation(
            f"Order value {estimated_order_value:.2f} exceeds allowed position value "
            f"{max_position_value:.2f}."
        )

    if portfolio.drawdown_percent >= limits.max_portfolio_drawdown_percent:
        raise RiskViolation("Portfolio drawdown circuit breaker is active.")

    daily_loss_limit = portfolio.total_value * limits.max_daily_loss_percent / 100
    if portfolio.daily_pnl <= -daily_loss_limit:
        raise RiskViolation("Daily loss circuit breaker is active.")

    existing_position = next(
        (position for position in portfolio.positions if position.symbol == order.symbol),
        None,
    )

    if existing_position is None and len(portfolio.positions) >= limits.max_open_positions:
        raise RiskViolation("Maximum number of open positions reached.")

    if order.side == "BUY" and estimated_order_value > portfolio.available_cash:
        raise RiskViolation("Insufficient available cash.")