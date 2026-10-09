from datetime import datetime, timezone


class NewsDataService:
    def get_news(self, symbol: str) -> list[dict]:
        return [
            {
                "symbol": symbol,
                "title": "No configured news provider",
                "summary": (
                    "News sentiment analysis is neutral because no licensed "
                    "news provider has been configured."
                ),
                "published_at": datetime.now(timezone.utc).isoformat(),
                "source": "system",
            }
        ]