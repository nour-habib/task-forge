from openai import OpenAI

from models.agent_output import AgentOutput


class BuilderAgent2:
    """
    The Bold Creative.
    Loud, expressive, and unforgettable. Makes things that stop you mid-scroll.
    Loves gradients, strong contrast, and designs that have personality.
    """

    SYSTEM_PROMPT = """
    You are a bold, expressive designer and developer. Your work is meant to be noticed.

    Design characteristics:
    - Vibrant, high-contrast colour palettes (gradients welcome)
    - Strong typographic hierarchy — mix weights and sizes with confidence
    - Dynamic layouts that break the grid when it serves the design
    - Expressive shapes, illustrations, or patterns as supporting elements
    - Designs should feel energetic and modern

    When given a job, write a short proposal explaining your bold creative approach,
    then produce the deliverable. Describe the energy and emotion you want the output to convey.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.name = "BuilderAgent2"
        self.persona = "The Bold Creative"

    def run(self, query: str) -> AgentOutput:
        """Execute the given query and return AgentOutput with generated image."""
        prompt_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT + "\n\nCreate a detailed image generation prompt (1-2 sentences) for DALL-E that captures your bold creative design approach for this request. Output ONLY the prompt, nothing else."},
                {"role": "user", "content": query},
            ],
        )
        image_prompt = prompt_response.choices[0].message.content.strip()

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
            prompt_or_job=query,
            style_notes=image_prompt,
        )
