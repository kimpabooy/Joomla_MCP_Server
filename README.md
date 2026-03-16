# MCP Server (Python)

FastAPI-projekt for Joomla 4 Core API med tva integrationsvägar:

1. Webb-UI med naturligt språk via LLM (`POST /chat`)
2. MCP-server for externa klienter (`/mcp`)

Projektet anropar Joomla API via verktyg i `mcp_tools.py`, och LLM valjer verktyg via OpenAI function calling.

Repo: `kimpabooy/Joomla_MCP_Server`  
Paketnamn: `joomla-mcp-server`  
Python: `>= 3.13`

---

## Arkitektur

```text
Browser UI (templates/index.html + static/chat.js)
     -> POST /chat
          -> src/routes/chat_router.py
               -> src/services/llm_service.py (OpenAI + tools schema)
               -> dispatch till verktyg i src/tools/mcp_tools.py
                    -> src/services/joomla_service.py
                         -> Joomla 4 Core API

Extern MCP-klient
     -> /mcp (FastMCP mount i main.py)
          -> src/tools/mcp_tools.py
               -> src/services/joomla_service.py
                    -> Joomla 4 Core API
```

---

## Endpoints

### App-routes

| Method | Endpoint | Purpose                                                            |
| ------ | -------- | ------------------------------------------------------------------ |
| `GET`  | `/`      | Renderar chat-UI (`templates/index.html`).                         |
| `POST` | `/chat`  | Tar emot prompt, låter LLM välja verktyg och kor Joomla-operation. |

### MCP-route

| Method     | Endpoint | Purpose                                                                   |
| ---------- | -------- | ------------------------------------------------------------------------- |
| ASGI mount | `/mcp`   | Exponerar FastMCP-verktyg for externa MCP-klienter (SSE/streamable HTTP). |

Notering: `/clear` hanteras på klientsidan i `static/chat.js` och rensar bara chatloggen i browsern.

---

## Tools (LLM + MCP)

Definierade i `src/tools/mcp_tools.py` och speglade som function-calling schema i `src/services/llm_service.py`.

| Tool             | Purpose                                          |
| ---------------- | ------------------------------------------------ |
| `list_articles`  | Hamta alla artiklar.                             |
| `get_article`    | Hamta artikel med ID.                            |
| `publish`        | Publicera artikel med ID.                        |
| `unpublish`      | Avpublicera artikel med ID.                      |
| `trash`          | Flytta artikel till papperskorg.                 |
| `create_article` | Skapa artikel med titel och innehall.            |
| `edit_article`   | Redigera artikel med ny titel och nytt innehall. |
| `remove_article` | Ta bort artikel permanent.                       |

---

## Projektstruktur

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

## Kom igang

### 1. Installera dependencies

```bash
uv sync
```

### 2. Konfigurera miljo

Skapa `.env` i projektroten:

```env
JOOMLA_URL=din_joomla_url_har
JOOMLA_API_TOKEN=din_token_har
OPENAI_API_KEY=din_openai_nyckel_har
```

### 3. Starta servern

```bash
uv run main.py
```

Server: `http://127.0.0.1:8000`

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
