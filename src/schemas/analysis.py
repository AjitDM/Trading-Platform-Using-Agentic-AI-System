from typing import Literal

from pydantic import BaseModel, Field


Direction = Literal["bullish", "bearish", "neutral"]


class AnalystOpinion(BaseModel):
    analyst: str
    direction: Direction
    confidence: float = Field(ge=0, le=1)
    thesis: str
    evidence: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


class AnalysisBundle(BaseModel):
    technical: AnalystOpinion | None = None
    fundamental: AnalystOpinion | None = None
    sentiment: AnalystOpinion | None = None
    portfolio: AnalystOpinion | None = None
    consensus: AnalystOpinion | None = None