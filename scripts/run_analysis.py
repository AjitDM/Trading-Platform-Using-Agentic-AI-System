import json
import sys

from src.graphs.trading_graph import start_trading_run


def main() -> None:
    symbol = sys.argv[1] if len(sys.argv) > 1 else "RELIANCE.NS"
    result = start_trading_run(symbol)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()