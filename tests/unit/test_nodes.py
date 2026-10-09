from src.nodes.signal_node import signal_node
from src.schemas.analysis import AnalysisBundle, AnalystOpinion
from src.schemas.market import MarketSnapshot
from src.schemas.portfolio import PortfolioSnapshot


def test_signal_node_holds_for_low_confidence() -> None:
    state = {
        "symbol": "RELIANCE.NS",
        "market": MarketSnapshot(
            symbol="RELIANCE.NS",
            last_price=1000,
            fetched_at="2026-01-01T00:00:00Z",
        ),
        "portfolio": PortfolioSnapshot(
            total_value=100_000,
            available_cash=100_000,
            daily_pnl=0,
            drawdown_percent=0,
        ),
        "analysis": AnalysisBundle(
            consensus=AnalystOpinion(
                analyst="consensus",
                direction="bullish",
                confidence=0.4,
                thesis="Weak evidence.",
            )
        ),
    }

    result = signal_node(state)

    assert result["signal"].action == "hold"
    assert result["signal"].quantity == 0