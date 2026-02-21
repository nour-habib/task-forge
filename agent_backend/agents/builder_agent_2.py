from openai import OpenAI


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

    def run(self, query: str) -> str:
        """Execute the given query and return the response."""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content
