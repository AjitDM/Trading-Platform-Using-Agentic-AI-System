from dataclasses import dataclass

from src.config.settings import get_settings


@dataclass(frozen=True)
class RiskLimits:
    max_position_percent: float
    max_daily_loss_percent: float
    max_portfolio_drawdown_percent: float
    max_open_positions: int
    max_order_value: float
    min_signal_confidence: float


def get_risk_limits() -> RiskLimits:
    settings = get_settings()

    return RiskLimits(
        max_position_percent=settings.max_position_percent,
        max_daily_loss_percent=settings.max_daily_loss_percent,
        max_portfolio_drawdown_percent=settings.max_portfolio_drawdown_percent,
        max_open_positions=settings.max_open_positions,
        max_order_value=settings.max_order_value,
        min_signal_confidence=settings.min_signal_confidence,
    )