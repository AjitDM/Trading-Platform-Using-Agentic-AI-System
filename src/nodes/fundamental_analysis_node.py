from src.llms.factory import get_analysis_llm
from src.prompts.fundamental import FUNDAMENTAL_ANALYSIS_PROMPT
from src.schemas.analysis import AnalystOpinion, AnalysisBundle
from src.states.state import TradingState
from src.tools.fundamental_tools import get_fundamental_summary


def fundamental_analysis_node(state: TradingState) -> dict:
    try:
        fundamental_context = get_fundamental_summary.invoke({"symbol": state["symbol"]})

        llm = get_analysis_llm().with_structured_output(AnalystOpinion)
        opinion = llm.invoke(
            FUNDAMENTAL_ANALYSIS_PROMPT.format(
                symbol=state["symbol"],
                fundamental_context=fundamental_context,
            )
        )

        opinion.analyst = "fundamental"

        bundle = state.get("analysis", AnalysisBundle())
        bundle.fundamental = opinion

        return {"analysis": bundle}
    except Exception as exc:
        neutral = AnalystOpinion(
            analyst="fundamental",
            direction="neutral",
            confidence=0.0,
            thesis="Fundamental analysis unavailable.",
            risks=[str(exc)],
        )
        bundle = state.get("analysis", AnalysisBundle())
        bundle.fundamental = neutral

        return {
            "analysis": bundle,
            "errors": [f"Fundamental analysis failed: {exc}"],
        }