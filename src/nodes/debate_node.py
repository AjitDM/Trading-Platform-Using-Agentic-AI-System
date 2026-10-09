from src.llms.factory import get_reasoning_llm
from src.prompts.debate import DEBATE_PROMPT
from src.schemas.analysis import AnalystOpinion, AnalysisBundle
from src.states.state import TradingState


def debate_node(state: TradingState) -> dict:
    bundle = state.get("analysis", AnalysisBundle())

    opinions = [
        opinion.model_dump()
        for opinion in [
            bundle.technical,
            bundle.fundamental,
            bundle.sentiment,
            bundle.portfolio,
        ]
        if opinion is not None
    ]

    if not opinions:
        return {"errors": ["Consensus generation skipped: no analyst opinions."]}

    try:
        llm = get_reasoning_llm().with_structured_output(AnalystOpinion)
        consensus = llm.invoke(
            DEBATE_PROMPT.format(opinions=opinions)
        )

        consensus.analyst = "consensus"
        bundle.consensus = consensus

        return {"analysis": bundle}
    except Exception as exc:
        neutral = AnalystOpinion(
            analyst="consensus",
            direction="neutral",
            confidence=0.0,
            thesis="Consensus analysis unavailable.",
            risks=[str(exc)],
        )
        bundle.consensus = neutral

        return {
            "analysis": bundle,
            "errors": [f"Consensus generation failed: {exc}"],
        }