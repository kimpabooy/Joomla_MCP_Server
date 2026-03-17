# MCP Server (Python)

FastAPI project for the Joomla 4 Core API with two integration paths:

1. Web UI natural language to the LLM (`POST /chat`)
2. MCP server for external clients (`/mcp`)

The project calls the Joomla API through tools in `mcp_tools.py`, and the LLM selects tools via OpenAI function calling.

Repo: `kimpabooy/Joomla_MCP_Server`  
Package name: `joomla-mcp-server`  
Python: `>= 3.13`

---

## Architecture

```text
Browser UI (templates/index.html + static/chat.js)
     -> POST /chat
          -> src/routes/chat_router.py
               -> src/services/llm_service.py (OpenAI + OPENAI_TOOL_SCHEMAS)
               -> server-side guardrails + TOOL_MAP dispatch
               -> src/tools/mcp_tools.py
                    -> src/services/joomla_service.py
                         -> Joomla 4 Core API

External MCP client
     -> /mcp (FastMCP mount in main.py)
          -> src/tools/mcp_tools.py
               -> src/services/joomla_service.py
                    -> Joomla 4 Core API
```

---

## Responsibilities (Tools)

Different kind of tool-names appear in multiple places, but each layer has a different responsibility.
Here are some explanation:

1. `src/services/llm_service.py`
   - `OPENAI_TOOL_SCHEMAS` Describes tools as OpenAI function-calling schema.
   - Purpose: Tells the model what tools are available and what kind of arguments are required.

2. `src/routes/chat_router.py`
   - `TOOL_MAP` Maps tool names from model output to Python callables.
   - Purpose: Runtime dispatch, execution flow, and confirmation guardrails.

3. `src/tools/mcp_tools.py`
   - `@mcp.tool()` Functions implement the actual Joomla operations.
   - Purpose: Business actions and MCP exposure for external clients.

In short:

- `llm_service.py` = Schema/Contract for planning
- `chat_router.py` = Orchestration and execution safety
- `mcp_tools.py` = Implementation

---

---

## Add a New Tool (Checklist)

When adding a tool, update all three layers:

1. Implement function in `src/tools/mcp_tools.py` (and decorate with `@mcp.tool()`).
2. Add schema entry in `OPENAI_TOOL_SCHEMAS` in `src/services/llm_service.py`.
3. Add dispatch entry in `TOOL_MAP` in `src/routes/chat_router.py`.
4. If destructive, add the tool name to `DESTRUCTIVE_TOOLS` in `src/routes/chat_router.py`.

This keeps chat flow and external MCP flow aligned.

---

## Endpoints

### App Routes

| Method | Endpoint | Purpose                                                                   |
| ------ | -------- | ------------------------------------------------------------------------- |
| `GET`  | `/`      | Renders the chat UI (`templates/index.html`).                             |
| `POST` | `/chat`  | Receives a prompt, lets the LLM choose tools, and runs Joomla operations. |

### MCP Route

| Method     | Endpoint | Purpose                                                               |
| ---------- | -------- | --------------------------------------------------------------------- |
| ASGI mount | `/mcp`   | Exposes FastMCP tools for external MCP clients (SSE/streamable HTTP). |

Note: `/clear` is handled on the client side in `static/chat.js` and only clears the chat log in the browser.

---

## Tools (LLM + MCP)

Defined in `src/tools/mcp_tools.py` and mirrored as function-calling schema in `src/services/llm_service.py`.

| Tool             | Purpose                                       |
| ---------------- | --------------------------------------------- |
| `list_articles`  | Fetch all articles.                           |
| `get_article`    | Fetch an article by ID.                       |
| `publish`        | Publish an article by ID.                     |
| `unpublish`      | Unpublish an article by ID.                   |
| `trash`          | Move an article to trash.                     |
| `create_article` | Create an article with title and content.     |
| `edit_article`   | Edit an article with a new title and content. |
| `remove_article` | Delete an article permanently.                |

---

## Project Structure

```text
├── main.py
├── pyproject.toml
├── .env
├── templates/
│   ├── index.html
├── static/
│   ├── chat.js
│   └── style.css
└── src/
    ├── routes/
    │   ├── chat_router.py
    └── services/
    │   ├── llm_service.py
    │   └── joomla_service.py
    └── tools/
        └── mcp_tools.py
```

---

## Getting Started

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure Environment

Create `.env` in the project root:

```env
JOOMLA_URL=your_joomla_url_here
JOOMLA_API_TOKEN=your_token_here
OPENAI_API_KEY=your_openai_key_here
```

### 3. Start the Server

```bash
uv run main.py
```

Local Server: `http://127.0.0.1:8000`

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
