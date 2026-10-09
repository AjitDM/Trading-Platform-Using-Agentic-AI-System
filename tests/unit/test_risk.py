import pytest

from src.risk.validators import RiskViolation, validate_order
from src.schemas.orders import OrderRequest
from src.schemas.portfolio import PortfolioSnapshot


def test_valid_order_passes_risk_check() -> None:
    portfolio = PortfolioSnapshot(
        total_value=100_000,
        available_cash=100_000,
        daily_pnl=0,
        drawdown_percent=0,
    )

    order = OrderRequest(
        symbol="RELIANCE.NS",
        side="BUY",
        quantity=5,
    )

    validate_order(
        order=order,
        portfolio=portfolio,
        current_price=1_000,
    )


def test_insufficient_cash_fails_risk_check() -> None:
    portfolio = PortfolioSnapshot(
        total_value=100_000,
        available_cash=100,
        daily_pnl=0,
        drawdown_percent=0,
    )

    order = OrderRequest(
        symbol="RELIANCE.NS",
        side="BUY",
        quantity=1,
    )

    with pytest.raises(RiskViolation, match="Insufficient available cash"):
        validate_order(
            order=order,
            portfolio=portfolio,
            current_price=1_000,
        )