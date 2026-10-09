from kiteconnect import KiteConnect

from src.brokers.base import Broker
from src.config.settings import get_settings
from src.schemas.orders import OrderRequest
from src.schemas.portfolio import PortfolioSnapshot, Position


class ZerodhaBroker(Broker):
    def __init__(self) -> None:
        self.settings = get_settings()

        if self.settings.trading_mode != "live":
            raise RuntimeError(
                "ZerodhaBroker requires TRADING_MODE=live. "
                "Use PaperBroker for all development and testing."
            )

        if not self.settings.zerodha_api_key or not self.settings.zerodha_access_token:
            raise RuntimeError("ZERODHA_API_KEY and ZERODHA_ACCESS_TOKEN are required.")

        self.kite = KiteConnect(api_key=self.settings.zerodha_api_key)
        self.kite.set_access_token(self.settings.zerodha_access_token)

    def get_portfolio(self) -> PortfolioSnapshot:
        margins = self.kite.margins(segment="equity")
        positions_data = self.kite.positions()["net"]

        positions = [
            Position(
                symbol=item["tradingsymbol"],
                quantity=int(item["quantity"]),
                average_price=float(item["average_price"] or 0.01),
                last_price=float(item["last_price"] or 0.01),
                unrealized_pnl=float(item["unrealised"] or 0.0),
            )
            for item in positions_data
            if int(item["quantity"]) != 0
        ]

        available_cash = float(margins["available"]["cash"])
        total_value = available_cash + sum(
            position.quantity * position.last_price for position in positions
        )

        return PortfolioSnapshot(
            total_value=max(total_value, 0.0),
            available_cash=max(available_cash, 0.0),
            daily_pnl=0.0,
            drawdown_percent=0.0,
            positions=positions,
        )

    def place_order(self, order: OrderRequest) -> dict:
        order_id = self.kite.place_order(
            variety=self.kite.VARIETY_REGULAR,
            exchange=order.exchange,
            tradingsymbol=order.symbol.replace(".NS", ""),
            transaction_type=order.side,
            quantity=order.quantity,
            product=order.product,
            order_type=order.order_type,
            price=order.price,
            trigger_price=order.trigger_price,
            validity=self.kite.VALIDITY_DAY,
            tag=order.tag,
        )

        return {
            "order_id": order_id,
            "status": "SUBMITTED",
            "broker": "zerodha",
        }

    def cancel_order(self, order_id: str) -> dict:
        self.kite.cancel_order(
            variety=self.kite.VARIETY_REGULAR,
            order_id=order_id,
        )
        return {
            "order_id": order_id,
            "status": "CANCELLED",
        }