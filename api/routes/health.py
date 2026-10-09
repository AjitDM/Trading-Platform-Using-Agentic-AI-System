from fastapi import APIRouter

from src.config.settings import get_settings

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    settings = get_settings()

    return {
        "status": "ok",
        "environment": settings.app_env,
        "trading_mode": settings.trading_mode,
        "broker_provider": settings.broker_provider,
    }