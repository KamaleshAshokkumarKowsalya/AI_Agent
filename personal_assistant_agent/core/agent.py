from __future__ import annotations

import os
from typing import Any

import google.generativeai as genai

from .memory_manager import MemoryManager
from .tool_registry import ToolRegistry


class Agent:
    """Personal assistant agent orchestrating Reason -> Act -> Observe iterations."""

    def __init__(
        self,
        memory: MemoryManager,
        tool_registry: ToolRegistry,
        model_name: str = "gemini-2.5-flash",
        max_iterations: int = 5,
    ) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY is not set. Please set it as an environment variable first."
            )

        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name=model_name)
        self._memory = memory
        self._tools = tool_registry
        self._max_iterations = max_iterations
        self._last_api_error: Exception | None = None

    def process_user_input(self, user_input: str) -> str:
        self._memory.add("user", user_input)

        system_prompt = (
            "You are a helpful personal assistant. "
            "Use available functions when needed for calculations, time, weather, "
            "file reading, or text analysis. "
            "If a function is needed, call exactly the appropriate function with valid arguments. "
            "If no function is needed, answer directly."
        )
        conversation_context = self._memory.render_context()
        initial_prompt = (
            f"{system_prompt}\n\n"
            f"Conversation History:\n{conversation_context}\n\n"
            f"Current User Request: {user_input}"
        )

        contents: list[Any] = [
            {
                "role": "user",
                "parts": [{"text": initial_prompt}],
            }
        ]
        tools_payload = [{"function_declarations": self._tools.get_declarations()}]

        final_text = ""
        for _ in range(self._max_iterations):
            response = self._safe_generate(contents=contents, tools_payload=tools_payload)
            if response is None:
                final_text = self._build_api_error_message()
                break

            function_call = self._extract_function_call(response)
            if function_call is None:
                final_text = self._extract_text(response)
                break

            tool_name, tool_args = function_call
            tool_output = self._tools.execute_tool(tool_name, tool_args)

            try:
                model_function_call_content = {
                    "role": "model",
                    "parts": [
                        {
                            "function_call": {
                                "name": tool_name,
                                "args": tool_args,
                            }
                        }
                    ],
                }
                function_response_content = {
                    "role": "function",
                    "parts": [
                        {
                            "function_response": {
                                "name": tool_name,
                                "response": tool_output,
                            }
                        }
                    ],
                }
                contents.extend([model_function_call_content, function_response_content])
            except Exception as exc:
                final_text = f"Function call handling failed: {exc}"
                break

        if not final_text:
            final_text = (
                "I couldn't complete the request within the iteration limit. "
                "Please try rephrasing or breaking the task into smaller steps."
            )

        self._memory.add("assistant", final_text)
        return final_text

    def _safe_generate(self, contents: list[Any], tools_payload: list[dict[str, Any]]) -> Any | None:
        try:
            self._last_api_error = None
            return self._model.generate_content(contents=contents, tools=tools_payload)
        except Exception as exc:
            self._last_api_error = exc
            print(f"[DEBUG] API Error: {type(exc).__name__}: {exc}")
            return None

    def _build_api_error_message(self) -> str:
        if self._last_api_error is None:
            return "I encountered an API error while processing your request."

        error_text = str(self._last_api_error).lower()

        if "quota" in error_text or "429" in error_text or "resourceexhausted" in error_text:
            return (
                "Gemini API quota is currently exceeded for this key/project. "
                "Please wait for reset or enable billing, then try again."
            )

        if "model" in error_text and ("not found" in error_text or "not supported" in error_text):
            return (
                "The configured Gemini model is unavailable for your account/API version. "
                "Use a supported model (for example gemini-2.5-flash) and retry."
            )

        if "api key" in error_text or "permission" in error_text or "unauthenticated" in error_text:
            return (
                "Authentication failed with Gemini API. "
                "Verify GEMINI_API_KEY and project permissions."
            )

        return "I encountered a Gemini API error while processing your request."

    @staticmethod
    def _extract_text(response: Any) -> str:
        if getattr(response, "text", None):
            return response.text

        parts = []
        try:
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    text = getattr(part, "text", "")
                    if text:
                        parts.append(text)
        except Exception:
            pass

        if parts:
            return "\n".join(parts)
        return "I have no textual response to return."

    @staticmethod
    def _extract_function_call(response: Any) -> tuple[str, dict[str, Any]] | None:
        try:
            candidates = getattr(response, "candidates", [])
            if not candidates:
                return None

            parts = candidates[0].content.parts
            for part in parts:
                function_call = getattr(part, "function_call", None)
                if function_call:
                    name = function_call.name
                    args = dict(function_call.args)
                    return name, args
            return None
        except Exception:
            return None
