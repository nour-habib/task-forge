"""
Shared Pydantic model for agent return values: image + metadata.
All builder agents can use this as their standard output type.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


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

    model_config = {"extra": "allow"}


class OrchestratorOutput(BaseModel):
    """Response model containing the 3 AgentOutput items from builder agents 1, 2, 3."""

    items: list[AgentOutput] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="The 3 AgentOutput items from builder agents 1, 2, 3",
    )
