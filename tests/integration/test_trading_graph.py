from src.graphs.graph_builder import build_trading_graph


def test_graph_compiles() -> None:
    graph = build_trading_graph()
    assert graph is not None