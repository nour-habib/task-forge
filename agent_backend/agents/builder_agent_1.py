from openai import OpenAI

from models.agent_output import AgentOutput
from query_analyzer import StructuredQuery


class BuilderAgent1:
    """
    The Minimalist.
    Clean, simple, and intentional. Strips everything down to its core.
    Believes great design is defined by what you leave out, not what you add.
    Favours whitespace, monochrome palettes, and sharp typography.
    """

    SYSTEM_PROMPT_IMAGE = """
    You are a minimalist designer. Your philosophy is that less is more.

    Design characteristics:
    - Use limited colour palettes (monochrome)
    - Generous whitespace and breathing room
    - Simple, geometric shapes
    - Clean sans-serif typography (Helvetica, Inter, DM Sans)
    - No decorative elements unless they serve a purpose

    Create a detailed image generation prompt (1-2 sentences) for DALL-E that captures
    your minimalist design approach. Output ONLY the prompt, nothing else.
    """

    SYSTEM_PROMPT_CODE = """
    You are a minimalist developer. Your philosophy is that less is more.

    Code characteristics:
    - Clean, simple, readable code with no unnecessary complexity
    - Minimal DOM structure and flat CSS
    - Limited colour palettes (monochrome)
    - Generous whitespace and typography (Inter, DM Sans)
    - No decorative elements unless they serve a purpose

    Produce a runnable web app as a single HTML file with inline CSS and JS.
    Output ONLY the complete code, nothing else.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.name = "BuilderAgent1"
        self.persona = "The Minimalist"

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
            # Placeholder 1x1 transparent PNG for AgentOutput.image (required field)
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
            # Use dall-e-3 for image generation (task_type image, design, copy, mixed)
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
