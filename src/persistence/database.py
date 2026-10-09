from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config.settings import get_settings


class Base(DeclarativeBase):
    pass


def get_engine():
    settings = get_settings()
    sync_url = settings.database_url.replace("+aiosqlite", "")
    return create_engine(sync_url, future=True)


SessionLocal = sessionmaker(
    bind=get_engine(),
    autocommit=False,
    autoflush=False,
    class_=Session,
)


def initialize_database() -> None:
    from src.persistence.models import TradingAuditRecord

    Base.metadata.create_all(bind=get_engine())