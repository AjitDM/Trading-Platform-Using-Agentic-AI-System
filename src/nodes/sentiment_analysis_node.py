from src.llms.factory import get_analysis_llm
from src.prompts.sentiment import SENTIMENT_ANALYSIS_PROMPT
from src.schemas.analysis import AnalystOpinion, AnalysisBundle
from src.states.state import TradingState


def sentiment_analysis_node(state: TradingState) -> dict:
    try:
        news = state.get("market").news if state.get("market") else []

        llm = get_analysis_llm().with_structured_output(AnalystOpinion)
        opinion = llm.invoke(
            SENTIMENT_ANALYSIS_PROMPT.format(
                symbol=state["symbol"],
                news=news,
            )
        )

        opinion.analyst = "sentiment"

        bundle = state.get("analysis", AnalysisBundle())
        bundle.sentiment = opinion

        return {"analysis": bundle}
    except Exception as exc:
        neutral = AnalystOpinion(
            analyst="sentiment",
            direction="neutral",
            confidence=0.0,
            thesis="Sentiment analysis unavailable.",
            risks=[str(exc)],
        )
        bundle = state.get("analysis", AnalysisBundle())
        bundle.sentiment = neutral

        return {
            "analysis": bundle,
            "errors": [f"Sentiment analysis failed: {exc}"],
        }