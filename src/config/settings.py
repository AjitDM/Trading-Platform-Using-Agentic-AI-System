from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Trading System"
    app_env: Literal["development", "test", "staging", "production"] = "development"
    log_level: str = "INFO"

    trading_mode: Literal["paper", "live"] = "paper"
    broker_provider: Literal["paper", "zerodha", "upstox"] = "paper"
    require_human_approval: bool = True

    exchange: str = "NSE"
    default_currency: str = "INR"
    paper_starting_cash: float = Field(default=100_000.0, gt=0)

    llm_gateway_url: str = "http://localhost:4000"
    llm_gateway_api_key: str = "sk-local-gateway-key"
    analysis_model: str = "analysis-model"
    reasoning_model: str = "reasoning-model"
    fallback_model: str = "fallback-model"

    market_data_provider: Literal["yfinance"] = "yfinance"
    news_api_key: str | None = None

    database_url: str = "sqlite+aiosqlite:///./trading.db"
    redis_url: str = "redis://localhost:6379/0"

    zerodha_api_key: str | None = None
    zerodha_api_secret: str | None = None
    zerodha_access_token: str | None = None

    upstox_access_token: str | None = None

    max_position_percent: float = Field(default=10.0, gt=0, le=100)
    max_daily_loss_percent: float = Field(default=2.0, gt=0, le=100)
    max_portfolio_drawdown_percent: float = Field(default=10.0, gt=0, le=100)
    max_open_positions: int = Field(default=10, ge=1)
    max_order_value: float = Field(default=10_000.0, gt=0)
    min_signal_confidence: float = Field(default=0.70, ge=0, le=1)

    langchain_tracing_v2: bool = False
    langchain_api_key: str | None = None
    langchain_project: str = "agentic-trading-system"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()