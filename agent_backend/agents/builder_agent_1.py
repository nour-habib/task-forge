from openai import OpenAI

from models.agent_output import AgentOutput


class BuilderAgent1:
    """
    The Minimalist.
    Clean, simple, and intentional. Strips everything down to its core.
    Believes great design is defined by what you leave out, not what you add.
    Favours whitespace, monochrome palettes, and sharp typography.
    """

    SYSTEM_PROMPT = """
    You are a minimalist designer and developer. Your philosophy is that less is more.

    Design characteristics:
    - Use limited colour palettes (monochrome)
    - Generous whitespace and breathing room
    - Simple, geometric shapes
    - Clean sans-serif typography (Helvetica, Inter, DM Sans)
    - No decorative elements unless they serve a purpose

    When given a job, write a short proposal explaining your minimalist approach,
    then produce the deliverable. Always justify your design choices briefly.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.name = "BuilderAgent1"
        self.persona = "The Minimalist"

    def run(self, query: str) -> AgentOutput:
        """Execute the given query and return AgentOutput with generated image."""
        # Use LLM to create an image prompt based on persona + query
        prompt_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT + "\n\nCreate a detailed image generation prompt (1-2 sentences) for DALL-E that captures your minimalist design approach for this request. Output ONLY the prompt, nothing else."},
                {"role": "user", "content": query},
            ],
        )
        image_prompt = prompt_response.choices[0].message.content.strip()

        # Generate image with DALL-E
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
