from datetime import datetime, timezone
from uuid import uuid4

from src.config.settings import get_settings
from src.schemas.orders import OrderRequest
from src.schemas.portfolio import PortfolioSnapshot


class PaperBroker:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.cash = self.settings.paper_starting_cash
        self.orders: list[dict] = []

    def get_portfolio(self) -> PortfolioSnapshot:
        return PortfolioSnapshot(
            total_value=self.cash,
            available_cash=self.cash,
            daily_pnl=0.0,
            drawdown_percent=0.0,
            positions=[],
        )

    def place_order(self, order: OrderRequest) -> dict:
        result = {
            "order_id": f"paper-{uuid4()}",
            "status": "PAPER_FILLED",
            "symbol": order.symbol,
            "exchange": order.exchange,
            "side": order.side,
            "quantity": order.quantity,
            "order_type": order.order_type,
            "product": order.product,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.orders.append(result)
        return result

    def cancel_order(self, order_id: str) -> dict:
        return {
            "order_id": order_id,
            "status": "PAPER_CANCELLED",
        }