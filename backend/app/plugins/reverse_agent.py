from ..agents import BaseAgent

class ReverseAgent(BaseAgent):
    """Agent that returns the reversed prompt."""

    async def run(self, prompt: str) -> str:
        return prompt[::-1]


def register():
    return {"reverse": ReverseAgent()}
