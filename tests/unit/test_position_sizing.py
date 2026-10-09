from src.risk.position_sizing import (
    calculate_fixed_fraction_quantity,
    calculate_risk_based_quantity,
)


def test_fixed_fraction_quantity() -> None:
    quantity = calculate_fixed_fraction_quantity(
        portfolio_value=100_000,
        entry_price=1_000,
        max_position_percent=10,
        max_order_value=20_000,
    )

    assert quantity == 10


def test_risk_based_quantity() -> None:
    quantity = calculate_risk_based_quantity(
        portfolio_value=100_000,
        entry_price=1_000,
        stop_loss=980,
        risk_per_trade_percent=1,
    )

    assert quantity == 50