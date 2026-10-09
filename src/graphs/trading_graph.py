from uuid import uuid4

from langgraph.types import Command

from src.graphs.graph_builder import build_trading_graph

graph = build_trading_graph()


def start_trading_run(symbol: str, timeframe: str = "1d") -> dict:
    run_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": run_id,
        }
    }

    initial_state = {
        "run_id": run_id,
        "symbol": symbol.upper(),
        "timeframe": timeframe,
        "messages": [],
        "errors": [],
    }

    result = graph.invoke(initial_state, config=config)

    return {
        "run_id": run_id,
        "result": result,
    }


def resume_trading_run(
    run_id: str,
    approved: bool,
    note: str | None = None,
) -> dict:
    config = {
        "configurable": {
            "thread_id": run_id,
        }
    }

    result = graph.invoke(
        Command(
            resume={
                "approved": approved,
                "note": note,
            }
        ),
        config=config,
    )

    return {
        "run_id": run_id,
        "result": result,
    }