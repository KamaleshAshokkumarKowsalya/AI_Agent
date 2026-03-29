from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from personal_assistant_agent.core.base_tool import BaseTool


class TimeTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_current_time"

    @property
    def description(self) -> str:
        return "Returns the current UTC date and time."

    def get_declaration(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {},
            },
        }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "ok": True,
            "timezone": "UTC",
            "iso": now.isoformat(),
            "human": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        }
