from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class BaseAgent(ABC):
    """Abstract base class for agents."""

    @abstractmethod
    async def run(self, prompt: str) -> str:
        """Process a prompt and return the agent's response."""
        raise NotImplementedError


class EchoAgent(BaseAgent):
    """Simple agent that echoes the prompt back."""

    async def run(self, prompt: str) -> str:
        return f"ECHO: {prompt}"


def get_default_agents() -> Dict[str, BaseAgent]:
    return {"echo": EchoAgent()}


AGENTS: Dict[str, BaseAgent] = get_default_agents()
