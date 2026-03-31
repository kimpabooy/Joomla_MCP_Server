# Joomla MCP Server

A modern FastAPI-based server for controlling and interacting with the Joomla 4 Core API using natural language and external clients.

## Features

- Chat UI where users can write questions/commands in natural language and have them executed against Joomla.
- Tools for articles, users, menus, tags, and redirects.
- LLM (OpenAI) interprets the user's question and automatically selects the correct tool.
- Server-side guardrails to protect against destructive actions without confirmation.
- Exposes the same tools via the MCP protocol for external systems.

## Architecture

```
Browser UI (templates/index.html + static/chat.js)
     -> POST /chat
          -> src/routes/chat_router.py
               -> src/services/llm_service.py (OpenAI + tool schema)
               -> TOOL_MAP dispatch
               -> src/tools/*_tool.py
                    -> respective src/services/*_service.py
                         -> Joomla 4 Core API

External MCP client
     -> /mcp (FastMCP mount in main.py)
          -> src/tools/*_tool.py etc.
               -> respective src/services/*_service.py
                    -> Joomla 4 Core API
```

## Layer Responsibilities

- **llm_service.py**: Describes available tools according to the OpenAI function-calling schema.
- **chat_router.py**: Orchestrates the flow, handles confirmations, and maps tool names to the correct Python function.
- **tools/\*\_tool.py**: Implements domain-specific operations (articles, users, menus, etc.).
- **services/\*\_service.py**: Communicates directly with the Joomla 4 Core API.

## Adding a New Tool

1. Implement the function in the appropriate `src/tools/*_tool.py` file.
2. Add a schema entry in `OPENAI_TOOL_SCHEMAS` in `src/services/llm_service.py`.
3. Add a dispatch entry in `TOOL_MAP` in `src/routes/chat_router.py`.
4. If the tool is destructive, add its name to `DESTRUCTIVE_TOOLS` in `chat_router.py`.

## Endpoints

| Method | Endpoint         | Purpose                                                        |
| ------ | ---------------- | -------------------------------------------------------------- |
| GET    | `/`              | Renders the chat UI (index.html)                               |
| POST   | `/chat`          | Receives prompt, lets LLM choose tool, and performs Joomla ops |
| GET    | `/joomla-status` | Returns JSON with online-status and link for yout joomla-site  |
| ASGI   | `/mcp`           | Exposes tools for external MCP clients                         |

## Logging

- Logging is configured in `src/config/logging_config.py` and initialized from `main.py`.
- Sensitive fields are masked before logging.
- Errors and events are logged for traceability.

## Development

- The project is modular and easy to extend with more tools/domains.
- Follow the checklist above to add new features.

## Project Structure

```text
├── main.py
├── pyproject.toml
├── templates/
│   └── index.html
├── static/
│   ├── chat.js
│   ├── style.css
│   └── favicon.ico
└── src/
     ├── config/
     │   └── logging_config.py
     ├── routes/
     │   └── chat_router.py
     ├── services/
     │   ├── joomla_API/
     |   |    ├── __init__.py
     │   │    └── *_service.py
     │   ├── __init__.py
     │   └── llm_service.py
     ├── tools/
     │   ├── __init__.py
     │   └── *_tool.py
     └── utils/
         ├── config.py
         └── formatters.py
```

## Getting Started

### 1. Install uv (if not already installed)

```bash
pip install uv
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment

Create `.env` in the project root:

```env
JOOMLA_API_URL=your_joomla_api_url_here
JOOMLA_API_TOKEN=your_joomla_api_token_here
JOOMLA_SITE_URL=your_joomla_site_url_here
OPENAI_API_KEY=your_openai_key_here
```

### 4. Start the Server

```bash
uv run main.py
```

Now runs on local Server: `http://127.0.0.1:8000`

---

## Dependencies

| Package         | Purpose                      |
| --------------- | ---------------------------- |
| `fastapi`       | Web framework                |
| `fastmcp`       | MCP server                   |
| `uvicorn`       | ASGI server                  |
| `jinja2`        | HTML templates               |
| `openai`        | LLM function calling         |
| `pydantic`      | Validation                   |
| `requests`      | Joomla HTTP calls            |
| `python-dotenv` | Environment variable loading |
