from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Message:
    role: str
    content: str


class MemoryManager:
    """In-memory conversation store for a single CLI session."""

    def __init__(self, max_turns: int = 20) -> None:
        self._messages: list[Message] = []
        self._max_turns = max_turns

    def add(self, role: str, content: str) -> None:
        self._messages.append(Message(role=role, content=content))
        self._trim()

    def history(self) -> list[Message]:
        return list(self._messages)

    def render_context(self) -> str:
        if not self._messages:
            return "No previous conversation."
        return "\n".join(f"{msg.role.title()}: {msg.content}" for msg in self._messages)

    def _trim(self) -> None:
        max_messages = self._max_turns * 2
        if len(self._messages) > max_messages:
            self._messages = self._messages[-max_messages:]
