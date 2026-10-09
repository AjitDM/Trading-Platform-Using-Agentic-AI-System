from datetime import datetime, timezone

import yfinance as yf

from src.schemas.market import MarketSnapshot, OHLCV
from src.tools.technical_tools import calculate_indicators


class MarketDataService:
    def get_snapshot(
        self,
        symbol: str,
        period: str = "6mo",
        interval: str = "1d",
    ) -> MarketSnapshot:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period, interval=interval, auto_adjust=False)

        if history.empty:
            raise ValueError(
                f"No OHLCV data returned for {symbol}. "
                "For NSE examples, use symbols such as RELIANCE.NS or TCS.NS."
            )

        history = history.dropna(subset=["Open", "High", "Low", "Close", "Volume"])

        candles = [
            OHLCV(
                timestamp=index.to_pydatetime(),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=float(row["Volume"]),
            )
            for index, row in history.tail(250).iterrows()
        ]

        return MarketSnapshot(
            symbol=symbol.upper(),
            last_price=candles[-1].close,
            candles=candles,
            indicators=calculate_indicators(history),
            fetched_at=datetime.now(timezone.utc),
        )