from typing import Any

import pandas as pd


def calculate_rsi(close: pd.Series, period: int = 14) -> float | None:
    if len(close) < period + 1:
        return None

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()

    if loss.iloc[-1] == 0:
        return 100.0

    rs = gain.iloc[-1] / loss.iloc[-1]
    return round(float(100 - (100 / (1 + rs))), 4)


def calculate_indicators(history: pd.DataFrame) -> dict[str, float]:
    close = history["Close"]

    indicators: dict[str, Any] = {
        "sma_20": float(close.tail(20).mean()) if len(close) >= 20 else float(close.mean()),
        "sma_50": float(close.tail(50).mean()) if len(close) >= 50 else float(close.mean()),
        "last_close": float(close.iloc[-1]),
        "return_20d_pct": (
            round(float((close.iloc[-1] / close.iloc[-21] - 1) * 100), 4)
            if len(close) >= 21
            else 0.0
        ),
    }

    rsi = calculate_rsi(close)
    if rsi is not None:
        indicators["rsi_14"] = rsi

    return {key: round(float(value), 4) for key, value in indicators.items()}