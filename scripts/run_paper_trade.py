import json
import sys

from src.config.settings import get_settings
from src.graphs.trading_graph import start_trading_run


def main() -> None:
    settings = get_settings()

    if settings.trading_mode != "paper":
        raise RuntimeError("This script may run only when TRADING_MODE=paper.")

    symbol = sys.argv[1] if len(sys.argv) > 1 else "RELIANCE.NS"
    result = start_trading_run(symbol)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()