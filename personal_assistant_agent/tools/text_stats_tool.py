from __future__ import annotations

import re
from typing import Any

from personal_assistant_agent.core.base_tool import BaseTool


class TextStatsTool(BaseTool):
    """Custom tool: computes lightweight text statistics."""

    @property
    def name(self) -> str:
        return "analyze_text"

    @property
    def description(self) -> str:
        return "Computes text statistics such as word, character, and sentence counts."

    def get_declaration(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze.",
                    }
                },
                "required": ["text"],
            },
        }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        text = str(kwargs["text"])

        words = re.findall(r"\b\w+\b", text)
        sentence_candidates = re.split(r"[.!?]+", text)
        sentence_count = len([s for s in sentence_candidates if s.strip()])

        return {
            "ok": True,
            "characters": len(text),
            "characters_no_spaces": len(text.replace(" ", "")),
            "word_count": len(words),
            "sentence_count": sentence_count,
            "average_word_length": round(
                sum(len(word) for word in words) / len(words), 2
            )
            if words
            else 0.0,
        }
