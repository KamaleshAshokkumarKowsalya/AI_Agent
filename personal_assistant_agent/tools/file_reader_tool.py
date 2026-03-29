from __future__ import annotations

from pathlib import Path
from typing import Any

from personal_assistant_agent.core.base_tool import BaseTool


class FileReaderTool(BaseTool):
    """Custom tool: reads local text files safely from workspace."""

    def __init__(self, workspace_root: str) -> None:
        self._workspace_root = Path(workspace_root).resolve()

    @property
    def name(self) -> str:
        return "read_local_file"

    @property
    def description(self) -> str:
        return "Reads a local UTF-8 text file from the current workspace."

    def get_declaration(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {
                        "type": "string",
                        "description": "Relative path to the file in the workspace.",
                    },
                    "max_chars": {
                        "type": "integer",
                        "description": "Maximum number of characters to return (100-20000, default 4000).",
                    },
                },
                "required": ["relative_path"],
            },
        }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        relative_path = str(kwargs["relative_path"]).strip()
        max_chars = int(kwargs.get("max_chars", 4000))
        max_chars = max(100, min(max_chars, 20000))

        candidate = (self._workspace_root / relative_path).resolve()
        if self._workspace_root not in candidate.parents and candidate != self._workspace_root:
            return {
                "ok": False,
                "error": "Path escapes workspace root and is not allowed.",
                "relative_path": relative_path,
            }

        if not candidate.exists():
            return {"ok": False, "error": "File not found.", "relative_path": relative_path}

        if candidate.is_dir():
            return {
                "ok": False,
                "error": "Provided path is a directory, expected a file.",
                "relative_path": relative_path,
            }

        try:
            text = candidate.read_text(encoding="utf-8")
            truncated = text[:max_chars]
            return {
                "ok": True,
                "relative_path": relative_path,
                "chars_returned": len(truncated),
                "truncated": len(text) > max_chars,
                "content": truncated,
            }
        except UnicodeDecodeError as exc:
            return {
                "ok": False,
                "error": "File is not valid UTF-8 text.",
                "details": str(exc),
                "relative_path": relative_path,
            }
        except OSError as exc:
            return {
                "ok": False,
                "error": "Failed to read file.",
                "details": str(exc),
                "relative_path": relative_path,
            }
