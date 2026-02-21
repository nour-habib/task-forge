from openai import OpenAI

from constants import DALL_E_IMAGE_SIZE, DALL_E_MODEL
from models.agent_output import AgentOutput


class BuilderAgent3:
    """
    The Pragmatist.
    Research-first, user-focused, and data-informed. Designs based on what works,
    not what looks cool. Prioritises accessibility, conversion, and usability.
    """

    SYSTEM_PROMPT = """
    You are a pragmatic, user-centred designer and developer. Every decision is justified by purpose.

    Design characteristics:
    - Colours chosen for accessibility and contrast ratios (WCAG compliant)
    - Layouts based on established UX patterns users already understand
    - Typography optimised for readability across screen sizes
    - Clear visual hierarchy that guides the user's eye naturally
    - Designs that convert and communicate, not just impress

    When given a job, write a short proposal explaining your pragmatic, user-first approach,
    then produce the deliverable. Reference any UX principles or best practices that informed your decisions.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.name = "BuilderAgent3"
        self.persona = "The Pragmatist"

    def run(self, query: str) -> AgentOutput:
        """Execute the given query and return AgentOutput with generated image."""
        prompt_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT + "\n\nCreate a detailed image generation prompt (1-2 sentences) for DALL-E that captures your pragmatic, user-centred design approach for this request. Output ONLY the prompt, nothing else."},
                {"role": "user", "content": query},
            ],
        )
        image_prompt = prompt_response.choices[0].message.content.strip()

        image_response = self.client.images.generate(
            model=DALL_E_MODEL,
            prompt=image_prompt,
            size=DALL_E_IMAGE_SIZE,
            response_format="b64_json",
        )
        b64_data = image_response.data[0].b64_json
        image_uri = f"data:image/png;base64,{b64_data}"

        return AgentOutput(
            image=image_uri,
            agent_name=self.name,
            persona=self.persona,
            prompt_or_job=query,
            style_notes=image_prompt,
        )
