from __future__ import annotations

from typing import Any

from personal_assistant_agent.core.base_tool import BaseTool


class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Performs basic arithmetic operations on two numbers."

    def get_declaration(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number."},
                    "b": {"type": "number", "description": "Second number."},
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "Arithmetic operation to apply.",
                    },
                },
                "required": ["a", "b", "operation"],
            },
        }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        a = float(kwargs["a"])
        b = float(kwargs["b"])
        operation = kwargs["operation"]

        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return {"ok": False, "error": "Division by zero is not allowed."}
            result = a / b
        else:
            return {"ok": False, "error": f"Unsupported operation: {operation}"}

        return {"ok": True, "operation": operation, "a": a, "b": b, "result": result}
