from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import analysis, approvals, health, trading
from src.persistence.database import initialize_database
from src.utils.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    initialize_database()
    yield


app = FastAPI(
    title="Agentic Trading System",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router, tags=["health"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(trading.router, prefix="/trading", tags=["trading"])
app.include_router(approvals.router, prefix="/approvals", tags=["approvals"])