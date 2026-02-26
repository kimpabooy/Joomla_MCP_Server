# MCP Server (Python)

En lättviktig **FastAPI**-server som exponerar ett litet “tools”-API (just nu **articles**) samt en enkel HTML-sida för att testa endpoints direkt i webbläsaren.

> Repo: `kimpabooy/MCP_Server_Py`  
> Paketnamn: `mcp-server-py` (från `pyproject.toml`)  
> Python: `>= 3.13`

---

## Vad projektet gör

Servern startar en FastAPI-app (`main.py`) med två grupper av routes:

- **API-routes** (`src/routes/mcp.py`)
  - `GET /articles` — returnerar en strukturerad respons med nuvarande lista av artiklar (i minnet)
  - `POST /add_article` — lägger till en ny artikel (JSON body) i listan (i minnet) och returnerar ett bekräftelsemeddelande

- **View-routes (HTML)** (`src/routes/views.py`)
  - `GET /` — serverar en enkel HTML-sida där du kan skriva in en endpoint (t.ex. `articles`, `add_article`) och navigera till den

Logiken för “articles tool” ligger i `src/tools/articles.py` och använder en Pydantic-modell (`MCPRequest`) för att returnera svar i ett konsekvent format:

## Projektstruktur
```json
├── main.py
├── pyproject.toml
└── src
    ├── routes
    │   ├── mcp.py
    │   └── views.py
    └── tools
        └── articles.py
```
