import math


def calculate_fixed_fraction_quantity(
    portfolio_value: float,
    entry_price: float,
    max_position_percent: float,
    max_order_value: float,
) -> int:
    if portfolio_value <= 0 or entry_price <= 0:
        return 0

    max_by_portfolio = portfolio_value * max_position_percent / 100
    capital_to_allocate = min(max_by_portfolio, max_order_value)

    return max(math.floor(capital_to_allocate / entry_price), 0)


def calculate_risk_based_quantity(
    portfolio_value: float,
    entry_price: float,
    stop_loss: float,
    risk_per_trade_percent: float = 1.0,
) -> int:
    if portfolio_value <= 0 or entry_price <= stop_loss:
        return 0

    maximum_loss = portfolio_value * risk_per_trade_percent / 100
    loss_per_share = entry_price - stop_loss

    return max(math.floor(maximum_loss / loss_per_share), 0)