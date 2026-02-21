"""
Shared Pydantic model for agent return values: image + metadata.
All builder agents can use this as their standard output type.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from models.judgment import AgentJudgment


class AgentOutput(BaseModel):
    """Metadata accompanying an agent-generated image."""

    image: str = Field(
        ..., description="Image as base64-encoded string (e.g. data URI or raw base64)"
    )
    agent_name: str = Field(
        ..., description="Name of the agent that produced the output"
    )
    persona: str = Field(..., description="Agent persona or style label")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    prompt_or_job: str | None = Field(
        None, description="User prompt or job description"
    )
    style_notes: str | None = Field(None, description="Optional style or design notes")
    extra: dict[str, Any] = Field(
        default_factory=dict, description="Additional key-value metadata"
    )
    score: float | None = Field(
        None, description="Judge's overall score (1-5) for this output"
    )

    model_config = {"extra": "allow"}


class OrchestratorOutput(BaseModel):
    """Response model containing the 3 AgentOutput items and their judgments."""

    items: list[AgentOutput] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="The 3 AgentOutput items from builder agents 1, 2, 3",
    )
    judgments: list[AgentJudgment] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="JudgeAgent ratings for each of the 3 builder outputs",
    )
