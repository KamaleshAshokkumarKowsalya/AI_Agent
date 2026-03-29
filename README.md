<<<<<<< HEAD
# AI_Agent
Adaptive CLI-based Personal Assistant AI Agent built with Python and Gemini function calling, featuring modular SOLID architecture (Agent, MemoryManager, ToolRegistry, BaseTool), ReAct reasoning loop, session memory, and pluggable tools (calculator, time, weather, file reader, text analyzer) with robust error handling.
=======
# Personal Assistant Agent (Gemini API)

This project implements an adaptive CLI-based AI Personal Assistant using the Google Gemini API with a modular architecture based on SOLID principles and GoF design patterns.

## Architecture

- **Agent** (`personal_assistant_agent/core/agent.py`)
  - Orchestrates the **Reason → Act → Observe** loop.
  - Decides whether to answer directly or call tools through Gemini function-calling.
- **MemoryManager** (`personal_assistant_agent/core/memory_manager.py`)
  - Stores and trims in-session conversation history.
- **ToolRegistry** (`personal_assistant_agent/core/tool_registry.py`)
  - Implements a dynamic **Registry/Factory** pattern for tool discovery and execution.
- **BaseTool** (`personal_assistant_agent/core/base_tool.py`)
  - Abstract interface enforcing consistent tool contracts (**OCP, DIP**).

## Implemented Tools

1. `calculator` - basic arithmetic operations
2. `get_current_time` - current UTC date/time
3. `get_weather` - weather lookup via wttr.in
4. `read_local_file` - **custom** tool to read local UTF-8 files from workspace safely
5. `analyze_text` - **custom** tool for text statistics

## Setup

1. Install Python 3.10+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set Gemini API key (recommended via `.env`):

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key
```

Alternative: set as environment variable directly:

### Windows (PowerShell)

```powershell
$env:GEMINI_API_KEY="your_api_key"
```

### Linux/macOS

```bash
export GEMINI_API_KEY="your_api_key"
```

Default model configured in the app: `gemini-2.5-flash`

## Run

```bash
python main.py
```

Type `exit` or `quit` to stop.

## Testing Suggestions

- Ask direct questions (no tools needed).
- Ask for calculations and current time.
- Ask for weather in valid and invalid city names.
- Ask the assistant to read a local file and summarize it.
- Trigger bad arguments or unknown requests to verify graceful error handling.
>>>>>>> 55043d2 (Added all files for AI_agent)
