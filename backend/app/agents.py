from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict
from pathlib import Path
import importlib


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


def load_plugins() -> Dict[str, BaseAgent]:
    """Load agent plugins from the plugins directory."""
    agents: Dict[str, BaseAgent] = {}
    plugins_dir = Path(__file__).resolve().parent / "plugins"
    if not plugins_dir.exists():
        return agents

    for file in plugins_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue
        module_name = f"app.plugins.{file.stem}"
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "register"):
                agents.update(module.register())
        except Exception as e:  # pragma: no cover - plugin failures shouldn't crash
            print(f"Failed to load plugin {file.name}: {e}")
    return agents


def get_default_agents() -> Dict[str, BaseAgent]:
    agents = {"echo": EchoAgent()}
    agents.update(load_plugins())
    return agents


AGENTS: Dict[str, BaseAgent] = get_default_agents()
