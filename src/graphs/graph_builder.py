import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from src.nodes.approval_node import approval_node
from src.nodes.audit_node import audit_node
from src.nodes.debate_node import debate_node
from src.nodes.execution_node import execution_node
from src.nodes.fundamental_analysis_node import fundamental_analysis_node
from src.nodes.market_data_node import market_data_node
from src.nodes.portfolio_node import portfolio_node
from src.nodes.risk_node import risk_node
from src.nodes.sentiment_analysis_node import sentiment_analysis_node
from src.nodes.signal_node import signal_node
from src.nodes.technical_analysis_node import technical_analysis_node
from src.states.state import TradingState


def route_after_signal(state: TradingState) -> str:
    signal = state.get("signal")

    if signal is None or signal.action == "hold" or signal.quantity == 0:
        return "audit"

    return "risk"


def route_after_risk(state: TradingState) -> str:
    if not state.get("risk_passed", False):
        return "audit"

    if state.get("approval_required", False):
        return "approval"

    return "execution"


def route_after_approval(state: TradingState) -> str:
    if state.get("approval_status") == "approved":
        return "execution"

    return "audit"


def build_trading_graph():
    builder = StateGraph(TradingState)

    builder.add_node("market_data", market_data_node)
    builder.add_node("portfolio", portfolio_node)
    builder.add_node("technical", technical_analysis_node)
    builder.add_node("fundamental", fundamental_analysis_node)
    builder.add_node("sentiment", sentiment_analysis_node)
    builder.add_node("debate", debate_node)
    builder.add_node("signal", signal_node)
    builder.add_node("risk", risk_node)
    builder.add_node("approval", approval_node)
    builder.add_node("execution", execution_node)
    builder.add_node("audit", audit_node)

    builder.add_edge(START, "market_data")
    builder.add_edge("market_data", "portfolio")
    builder.add_edge("portfolio", "technical")
    builder.add_edge("technical", "fundamental")
    builder.add_edge("fundamental", "sentiment")
    builder.add_edge("sentiment", "debate")
    builder.add_edge("debate", "signal")

    builder.add_conditional_edges(
        "signal",
        route_after_signal,
        {
            "risk": "risk",
            "audit": "audit",
        },
    )

    builder.add_conditional_edges(
        "risk",
        route_after_risk,
        {
            "approval": "approval",
            "execution": "execution",
            "audit": "audit",
        },
    )

    builder.add_conditional_edges(
        "approval",
        route_after_approval,
        {
            "execution": "execution",
            "audit": "audit",
        },
    )

    builder.add_edge("execution", "audit")
    builder.add_edge("audit", END)

    connection = sqlite3.connect(
        "trading-checkpoints.db",
        check_same_thread=False,
    )
    checkpointer = SqliteSaver(connection)

    return builder.compile(checkpointer=checkpointer)