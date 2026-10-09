from src.llms.factory import get_analysis_llm
from src.prompts.technical import TECHNICAL_ANALYSIS_PROMPT
from src.schemas.analysis import AnalystOpinion, AnalysisBundle
from src.states.state import TradingState


def technical_analysis_node(state: TradingState) -> dict:
    if "market" not in state:
        return {"errors": ["Technical analysis skipped: market data missing."]}

    try:
        llm = get_analysis_llm().with_structured_output(AnalystOpinion)

        opinion = llm.invoke(
            TECHNICAL_ANALYSIS_PROMPT.format(
                market_data=state["market"].model_dump_json(),
            )
        )

        opinion.analyst = "technical"

        bundle = state.get("analysis", AnalysisBundle())
        bundle.technical = opinion

        return {"analysis": bundle}
    except Exception as exc:
        neutral = AnalystOpinion(
            analyst="technical",
            direction="neutral",
            confidence=0.0,
            thesis="Technical analysis unavailable due to LLM or data failure.",
            risks=[str(exc)],
        )
        bundle = state.get("analysis", AnalysisBundle())
        bundle.technical = neutral

        return {
            "analysis": bundle,
            "errors": [f"Technical analysis failed: {exc}"],
        }