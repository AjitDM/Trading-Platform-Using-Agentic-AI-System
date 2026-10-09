from src.brokers.base import Broker
from src.schemas.orders import OrderRequest
from src.schemas.portfolio import PortfolioSnapshot


class UpstoxBroker(Broker):
    def __init__(self) -> None:
        raise NotImplementedError(
            "Upstox broker adapter is intentionally not implemented yet. "
            "Use PaperBroker or implement this adapter only after validating "
            "the application with paper trading."
        )

    def get_portfolio(self) -> PortfolioSnapshot:
        raise NotImplementedError

    def place_order(self, order: OrderRequest) -> dict:
        raise NotImplementedError

    def cancel_order(self, order_id: str) -> dict:
        raise NotImplementedError