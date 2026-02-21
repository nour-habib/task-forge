"""
JudgeAgent: evaluates the work of the 3 builder agents using a 5-point criteria.
"""

import json
from openai import OpenAI

from models.agent_output import AgentOutput
from models.judgment import (
    AgentJudgment,
    CriterionRating,
    JudgeOutput,
    JUDGE_CRITERIA,
)


class JudgeAgent:
    """
    Judges the work of the 3 builder agents.
    Applies a 5-point rating on: relevance, creativity, persona_consistency,
    aesthetic_quality, technical_execution.
    """

    SYSTEM_PROMPT = """You are an expert design critic. Evaluate each builder agent's image output against these 5 criteria (score 1-5 each):
1. relevance - How well does the image match the prompt/requirements?
2. creativity - Originality and imagination
3. persona_consistency - Does it align with the agent's stated style/persona?
4. aesthetic_quality - Visual appeal, composition, balance
5. technical_execution - Clarity, coherence, polish

Score each criterion 1-5 (1=poor, 5=excellent). Provide a brief rationale for each.
Compute overall_score as the average of the 5 criterion scores (round to 1 decimal).
Write a short summary (1-2 sentences) of your overall assessment.

Output valid JSON only, with this exact shape:
{{
  "agent_name": "string",
  "persona": "string",
  "criteria_ratings": [
    {{"criterion": "relevance", "score": 1-5, "rationale": "..."}},
    {{"criterion": "creativity", "score": 1-5, "rationale": "..."}},
    {{"criterion": "persona_consistency", "score": 1-5, "rationale": "..."}},
    {{"criterion": "aesthetic_quality", "score": 1-5, "rationale": "..."}},
    {{"criterion": "technical_execution", "score": 1-5, "rationale": "..."}}
  ],
  "overall_score": 1.0-5.0,
  "summary": "string"
}"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def _judge_one(self, output: AgentOutput, prompt_or_job: str) -> AgentJudgment:
        """Judge a single builder agent's output."""
        # Build message with image - use the image URL from AgentOutput
        image_url = output.image if output.image.startswith("data:") else f"data:image/png;base64,{output.image}"

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Evaluate this image from {output.agent_name} (persona: {output.persona}).
Style notes: {output.style_notes or 'N/A'}
Original prompt/job: {prompt_or_job}

Provide your judgment as JSON.""",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                },
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        data = json.loads(content)

        # Ensure criteria_ratings has exactly 5 items in the right order
        ratings = []
        for c in JUDGE_CRITERIA:
            found = next((r for r in data.get("criteria_ratings", []) if r.get("criterion") == c), None)
            if found:
                ratings.append(CriterionRating(**found))
            else:
                ratings.append(CriterionRating(criterion=c, score=3, rationale="Not specified"))

        return AgentJudgment(
            agent_name=data.get("agent_name", output.agent_name),
            persona=data.get("persona", output.persona),
            criteria_ratings=ratings[:5],
            overall_score=round(float(data.get("overall_score", 3.0)), 1),
            summary=data.get("summary", "No summary provided."),
        )

    def judge(self, outputs: list[AgentOutput], prompt_or_job: str) -> JudgeOutput:
        """
        Judge the work of the 3 builder agents.
        Returns JudgeOutput with ratings for each based on the 5-point criteria.
        """
        if len(outputs) != 3:
            raise ValueError("JudgeAgent expects exactly 3 builder outputs")
        judgments = [
            self._judge_one(output, prompt_or_job)
            for output in outputs
        ]
        return JudgeOutput(judgments=judgments)
