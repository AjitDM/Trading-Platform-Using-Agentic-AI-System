from functools import lru_cache

from src.brokers.base import Broker
from src.brokers.paper_broker import PaperBroker
from src.config.settings import get_settings


@lru_cache
def get_broker() -> Broker:
    settings = get_settings()

    if settings.broker_provider == "paper":
        return PaperBroker()

    if settings.broker_provider == "zerodha":
        from src.brokers.zerodha_broker import ZerodhaBroker

        return ZerodhaBroker()

    if settings.broker_provider == "upstox":
        from src.brokers.upstox_broker import UpstoxBroker

        return UpstoxBroker()

    raise ValueError(f"Unsupported broker provider: {settings.broker_provider}")