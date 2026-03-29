from __future__ import annotations

from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> bool:
        return False

from personal_assistant_agent.core.agent import Agent
from personal_assistant_agent.core.memory_manager import MemoryManager
from personal_assistant_agent.core.tool_registry import ToolRegistry
from personal_assistant_agent.tools.calculator_tool import CalculatorTool
from personal_assistant_agent.tools.file_reader_tool import FileReaderTool
from personal_assistant_agent.tools.text_stats_tool import TextStatsTool
from personal_assistant_agent.tools.time_tool import TimeTool
from personal_assistant_agent.tools.weather_tool import WeatherTool


load_dotenv()


def build_agent() -> Agent:
    workspace_root = str(Path(__file__).parent.resolve())

    memory = MemoryManager(max_turns=30)
    registry = ToolRegistry()

    registry.register(CalculatorTool())
    registry.register(TimeTool())
    registry.register(WeatherTool())
    registry.register(FileReaderTool(workspace_root=workspace_root))
    registry.register(TextStatsTool())

    return Agent(memory=memory, tool_registry=registry)


def run_cli() -> None:
    try:
        agent = build_agent()
    except EnvironmentError as exc:
        print(f"Startup error: {exc}")
        return
    except Exception as exc:
        print(f"Unexpected startup error: {exc}")
        return

    print("Personal Assistant Agent (Gemini + Tools)")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            response = agent.process_user_input(user_input)
            print(f"Assistant: {response}\n")
        except Exception as exc:
            print(f"Assistant: I hit an unexpected error: {exc}\n")


if __name__ == "__main__":
    run_cli()
