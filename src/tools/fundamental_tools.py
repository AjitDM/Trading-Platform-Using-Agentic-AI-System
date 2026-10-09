from langchain_core.tools import tool


@tool
def get_fundamental_summary(symbol: str) -> dict:
    """Return a safe placeholder until a licensed fundamentals provider is integrated."""
    return {
        "symbol": symbol,
        "available": False,
        "message": (
            "No licensed fundamental data provider is configured. "
            "Do not infer or fabricate financial metrics."
        ),
    }