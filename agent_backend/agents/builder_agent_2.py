from openai import OpenAI

from models.agent_output import AgentOutput
from query_analyzer import StructuredQuery


class BuilderAgent2:
    """
    The Bold Creative.
    Loud, expressive, and unforgettable. Makes things that stop you mid-scroll.
    Loves gradients, strong contrast, and designs that have personality.
    """

    SYSTEM_PROMPT_IMAGE = """
    You are a bold, expressive designer. Your work is meant to be noticed.

    Design characteristics:
    - Vibrant, high-contrast colour palettes (gradients welcome)
    - Strong typographic hierarchy — mix weights and sizes with confidence
    - Dynamic layouts that break the grid when it serves the design
    - Expressive shapes, illustrations, or patterns as supporting elements
    - Designs should feel energetic and modern

    Create a detailed image generation prompt (1-2 sentences) for DALL-E that captures
    your bold creative design approach. Output ONLY the prompt, nothing else.
    """

    SYSTEM_PROMPT_CODE = """
    You are a bold, expressive developer. Your work is meant to be noticed.

    Code characteristics:
    - Vibrant, high-contrast colour palettes and gradients in CSS
    - Strong typographic hierarchy with varied weights and sizes
    - Dynamic layouts that break the grid when it serves the design
    - Expressive shapes, animations, or patterns as supporting elements
    - Code that feels energetic and modern

    Produce a runnable web app as a single HTML file with inline CSS and JS.
    Output ONLY the complete code, nothing else.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.name = "BuilderAgent2"
        self.persona = "The Bold Creative"

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
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                response_format="b64_json",
                quality="standard",
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
