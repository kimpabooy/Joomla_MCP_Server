# MCP Server (Python)

En lättviktig **FastAPI**-server som fungerar som ett MCP-lager (Model Context Protocol) mot **Joomla 4 Core API**. Servern exponerar ett "tools"-API för **articles** samt ett webb-UI med chatt för att testa endpoints direkt i webbläsaren.

> Repo: `kimpabooy/MCP_Server_Py`  
> Paketnamn: `mcp-server-py` (från `pyproject.toml`)  
> Python: `>= 3.13`

---

## Arkitektur

Projektet följer en trelagersarkitektur:

```
Webbläsare (Chat UI)
  → Proxy (/mcp-proxy) — bestämmer HTTP-metod via regex
    → Routes (mcp.py) — FastAPI-endpoints med validering
      → Tools (articles.py) — formatering + MCPRequest-modell
        → Services (joomla_service.py) — HTTP-anrop mot Joomla API
```

Chat-UI:t skickar alla kommandon som `GET` via `fetch()`. Proxyn analyserar endpoint-mönstret med regex och vidarebefordrar requesten med rätt HTTP-metod (GET/POST/PATCH/DELETE) till de lokala routerna.

---

## Endpoints

### API-routes (`src/routes/mcp.py`)

| Metod | Endpoint                   | Beskrivning                         |
| ----- | -------------------------- | ----------------------------------- |
| GET   | `/help`                    | Listar alla tillgängliga endpoints  |
| GET   | `/articles`                | Hämtar alla artiklar                |
| GET   | `/articles/{id}`           | Hämtar en specifik artikel          |
| PATCH | `/articles/{id}/publish`   | Publicerar en artikel               |
| PATCH | `/articles/{id}/unpublish` | Avpublicerar en artikel             |
| PATCH | `/articles/{id}/trash`     | Slänger en artikel i papperskorgen  |
| \*    | `/mcp-proxy?endpoint=...`  | Proxy — översätter GET → rätt metod |

### View-routes (`src/routes/views.py`)

| Metod | Endpoint | Beskrivning                       |
| ----- | -------- | --------------------------------- |
| GET   | `/`      | Huvudsida med chatt-UI            |
| GET   | `/clear` | Rensar chatten (returnerar index) |

---

## Projektstruktur

```
├── main.py                  # FastAPI app + uvicorn
├── pyproject.toml
├── .env                     # JOOMLA_URL, JOOMLA_API_TOKEN
├── templates/
│   ├── index.html           # Chatt-UI (Jinja2-template)
│   └── add_article.html     # Formulär för att skapa artikel
├── static/
│   ├── style.css            # All CSS
│   └── chat.js              # Chat-logik (fetch → proxy)
└── src/
    ├── routes/
    │   ├── mcp.py           # API-routes + proxy + Pydantic-modeller
    │   └── views.py         # Jinja2 template-rendering
    ├── tools/
    │   └── articles.py      # Formatering + MCPRequest-wrapper
    └── services/
        └── joomla_service.py  # HTTP-anrop mot Joomla REST API
```

---

## Kom igång

### 1. Installera dependencies

```bash
uv sync
```

### 2. Konfigurera miljövariabler

Skapa en `.env`-fil i projektets rot:

```env
JOOMLA_URL=http://localhost:8080/api/index.php/v1
JOOMLA_API_TOKEN=din_token_här
```

### 3. Starta servern

```bash
uv run main.py
```

Servern körs på `http://127.0.0.1:8000`.

---

## Dependencies

| Paket         | Syfte                          |
| ------------- | ------------------------------ |
| fastapi       | Web-framework                  |
| uvicorn       | ASGI-server                    |
| jinja2        | HTML-templates                 |
| pydantic      | Validering av request/response |
| requests      | HTTP-anrop mot Joomla API      |
| python-dotenv | Läser `.env`-filer             |
