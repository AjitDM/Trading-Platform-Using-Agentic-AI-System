from abc import ABC, abstractmethod

from src.schemas.orders import OrderRequest
from src.schemas.portfolio import PortfolioSnapshot


class Broker(ABC):
    @abstractmethod
    def get_portfolio(self) -> PortfolioSnapshot:
        raise NotImplementedError

    @abstractmethod
    def place_order(self, order: OrderRequest) -> dict:
        raise NotImplementedError

    @abstractmethod
    def cancel_order(self, order_id: str) -> dict:
        raise NotImplementedError