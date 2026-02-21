from openai import OpenAI


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
