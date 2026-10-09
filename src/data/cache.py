import json
from typing import Any

from redis import Redis

from src.config.settings import get_settings


class CacheService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = Redis.from_url(
            self.settings.redis_url,
            decode_responses=True,
        )

    def get_json(self, key: str) -> dict[str, Any] | None:
        value = self.client.get(key)
        return json.loads(value) if value else None

    def set_json(self, key: str, value: dict[str, Any], ttl_seconds: int = 60) -> None:
        self.client.setex(key, ttl_seconds, json.dumps(value, default=str))