"""
Models for JudgeAgent ratings of builder agent outputs.
"""

from pydantic import BaseModel, Field


# 5-point criteria for judging builder outputs
JUDGE_CRITERIA = [
    "relevance",           # How well the output matches the prompt/requirements
    "creativity",          # Originality and imagination
    "persona_consistency", # Alignment with the agent's stated style
    "aesthetic_quality",   # Visual appeal and composition
    "technical_execution", # Clarity, coherence, polish
]


class CriterionRating(BaseModel):
    """A single criterion rated 1-5."""

    criterion: str = Field(..., description="Name of the criterion")
    score: int = Field(..., ge=1, le=5, description="Score from 1 to 5")
    rationale: str = Field(..., description="Brief justification for the score")


class AgentJudgment(BaseModel):
    """Judgment for one builder agent's output."""

    agent_name: str = Field(..., description="Name of the agent judged")
    persona: str = Field(..., description="Agent persona")
    criteria_ratings: list[CriterionRating] = Field(
        ...,
        min_length=5,
        max_length=5,
        description="Ratings for the 5 criteria",
    )
    overall_score: float = Field(
        ...,
        ge=1.0,
        le=5.0,
        description="Average of criteria scores",
    )
    summary: str = Field(..., description="Brief overall assessment")


class JudgeOutput(BaseModel):
    """Output from JudgeAgent: judgments for all 3 builder agents."""

    judgments: list[AgentJudgment] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Judgment for each of the 3 builder agents",
    )
