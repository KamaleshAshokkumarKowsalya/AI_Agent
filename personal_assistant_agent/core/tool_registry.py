from __future__ import annotations

from typing import Any

from .base_tool import BaseTool


class ToolRegistry:
    """Registry/factory for tools to avoid hardcoded if-else dispatching."""

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")
        self._tools[tool.name] = tool

    def get_declarations(self) -> list[dict[str, Any]]:
        return [tool.get_declaration() for tool in self._tools.values()]

    def execute_tool(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        tool = self._tools.get(tool_name)
        if not tool:
            return {
                "ok": False,
                "error": f"Unknown tool requested: '{tool_name}'.",
                "tool": tool_name,
            }

        try:
            return tool.execute(**args)
        except TypeError as exc:
            return {
                "ok": False,
                "error": "Invalid arguments provided for tool execution.",
                "details": str(exc),
                "tool": tool_name,
                "received_args": args,
            }
        except Exception as exc:
            return {
                "ok": False,
                "error": "Tool execution failed due to an unexpected error.",
                "details": str(exc),
                "tool": tool_name,
            }
