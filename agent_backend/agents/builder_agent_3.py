from openai import OpenAI

from constants import DALL_E_IMAGE_SIZE, IMAGE_MODEL, IMAGE_MODEL_QUALITY
from models.agent_output import AgentOutput
from query_analyzer import StructuredQuery


class BuilderAgent3:
    """
    The Pragmatist.
    Research-first, user-focused, and data-informed. Designs based on what works,
    not what looks cool. Prioritises accessibility, conversion, and usability.
    """

    SYSTEM_PROMPT_IMAGE = """
    You are a pragmatic, user-centred designer. Every decision is justified by purpose.

    Design characteristics:
    - Colours chosen for accessibility and contrast ratios (WCAG compliant)
    - Layouts based on established UX patterns users already understand
    - Typography optimised for readability across screen sizes
    - Clear visual hierarchy that guides the user's eye naturally
    - Designs that convert and communicate, not just impress

    Create a detailed image generation prompt (1-2 sentences) for DALL-E that captures
    your pragmatic, user-centred design approach. Output ONLY the prompt, nothing else.
    """

    SYSTEM_PROMPT_CODE = """
    You are a pragmatic, user-centred developer. Every decision is justified by purpose.

    Code characteristics:
    - Colours and contrast ratios WCAG compliant
    - Semantic HTML and accessible patterns (ARIA when needed)
    - Typography optimised for readability across screen sizes
    - Clear visual hierarchy and simple, maintainable code
    - Focus on conversion and usability, not flashy effects

    Produce a runnable web app as a single HTML file with inline CSS and JS.
    Output ONLY the complete code, nothing else.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.name = "BuilderAgent3"
        self.persona = "The Pragmatist"

    def run(self, structured_query: StructuredQuery) -> AgentOutput:
        """Execute the given query and return AgentOutput (image or code based on task_type)."""
        query = structured_query.to_agent_prompt()

        if structured_query.task_type == "code":
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT_CODE},
                    {"role": "user", "content": query},
                ],
            )
            content = response.choices[0].message.content
            code = content.strip() if content else ""
            placeholder = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
            return AgentOutput(
                image=placeholder,
                agent_name=self.name,
                persona=self.persona,
                prompt_or_job=structured_query.raw_query,
                style_notes="Code output",
                extra={"code": code},
            )
        else:
            prompt_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT_IMAGE},
                    {"role": "user", "content": query},
                ],
            )
            image_prompt = (prompt_response.choices[0].message.content or "").strip()

            image_response = self.client.images.generate(
                model=IMAGE_MODEL,
                prompt=image_prompt,
                size=DALL_E_IMAGE_SIZE,
                quality=IMAGE_MODEL_QUALITY,
            )
            b64_data = image_response.data[0].b64_json
            image_uri = f"data:image/png;base64,{b64_data}"
            return AgentOutput(
                image=image_uri,
                agent_name=self.name,
                persona=self.persona,
                prompt_or_job=structured_query.raw_query,
                style_notes=image_prompt,
            )
