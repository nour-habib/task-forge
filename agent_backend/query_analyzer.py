"""
Query analysis: parse user query, infer intent, and produce a structured query
for builder agents.
"""

from openai import OpenAI
from pydantic import BaseModel, Field


class StructuredQuery(BaseModel):
    """Structured representation of a user query for agents."""

    intent: str = Field(
        ...,
        description="Short label for what the user wants (e.g. design_landing_page, build_component, create_image).",
    )
    task_type: str = Field(
        ...,
        description="Category: design, code, image, copy, or mixed.",
    )
    requirements: list[str] = Field(
        default_factory=list,
        description="Key things the deliverable must do or include.",
    )
    constraints: list[str] = Field(
        default_factory=list,
        description="Limits or rules (e.g. mobile-first, no animations).",
    )
    raw_query: str = Field(
        ...,
        description="Original user query preserved for reference.",
    )

    def to_agent_prompt(self) -> str:
        """Format this structured query into a single prompt string for builder agents."""
        parts = [f"Intent: {self.intent}", f"Task type: {self.task_type}"]
        if self.requirements:
            parts.append("Requirements: " + "; ".join(self.requirements))
        if self.constraints:
            parts.append("Constraints: " + "; ".join(self.constraints))
        parts.append(f"Original request: {self.raw_query}")
        return "\n".join(parts)


class QueryAnalyzer:
    """
    Parses a user query, infers intent, and returns a StructuredQuery
    that agents can consume.
    """

    SYSTEM_PROMPT = """You are a query analyst. Given a user request, you extract intent and structure it for design/code agents.

Output valid JSON only, with this exact shape (no extra fields):
{
  "intent": "short_snake_case_label",
  "task_type": "code" | "image" | "other",
  "requirements": ["requirement 1", "requirement 2"],
  "constraints": ["constraint 1"],
  "raw_query": "the original user query exactly as given"
}

- intent: one short label (e.g. design_landing_page, build_react_form, create_hero_image).
- task_type: design (UI/UX), code (components/APIs), image (visuals), copy (text), or mixed.
- requirements: list of must-haves from the user (can be empty []).
- constraints: limits or rules (e.g. "mobile-first", "no external APIs") (can be empty []).
- raw_query: copy the user's message exactly.

Output only the JSON object, no markdown or explanation."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze(self, user_query: str) -> StructuredQuery:
        """
        Parse the user query and return a StructuredQuery with intent and structured fields.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_query},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            return StructuredQuery(
                intent="unknown",
                task_type="mixed",
                raw_query=user_query,
            )
        # Strip markdown code fence if present
        text = content.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        return StructuredQuery.model_validate_json(text)
