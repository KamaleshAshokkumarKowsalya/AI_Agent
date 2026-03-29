from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Abstract tool interface for all agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique tool name used for registry and function calling."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a short description of the tool capability."""

    @abstractmethod
    def get_declaration(self) -> dict[str, Any]:
        """Return Gemini function declaration schema for this tool."""

    @abstractmethod
    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute the tool and return structured output."""
