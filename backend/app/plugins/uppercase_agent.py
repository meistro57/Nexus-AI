from ..agents import BaseAgent

class UppercaseAgent(BaseAgent):
    """Agent that returns the prompt in uppercase."""

    async def run(self, prompt: str) -> str:
        return prompt.upper()


def register():
    return {"uppercase": UppercaseAgent()}
