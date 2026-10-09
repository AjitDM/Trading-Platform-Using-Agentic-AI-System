from src.brokers.paper_broker import PaperBroker
from src.schemas.orders import OrderRequest


def test_paper_broker_places_order() -> None:
    broker = PaperBroker()

    result = broker.place_order(
        OrderRequest(
            symbol="RELIANCE.NS",
            side="BUY",
            quantity=1,
        )
    )

    assert result["status"] == "PAPER_FILLED"
    assert result["symbol"] == "RELIANCE.NS"