# Joomla MCP Server

En modern FastAPI-baserad server för att styra och interagera med Joomla 4 Core API via naturligt språk och externa klienter.

## Funktionalitet

- Chat-UI där användaren kan skriva frågor/kommandon på naturligt språk och få dem utförda mot Joomla.
- Verktyg ("tools") för artiklar, användare, menyer, taggar och omdirigeringar.
- LLM (OpenAI) tolkar användarens fråga och väljer rätt verktyg automatiskt.
- Server-side guardrails för att skydda mot destruktiva åtgärder utan bekräftelse.
- Exponering av samma verktyg via MCP-protokollet för externa system.

## Arkitektur

```
Browser UI (templates/index.html + static/chat.js)
     -> POST /chat
          -> src/routes/chat_router.py
               -> src/services/llm_service.py (OpenAI + verktygs-schema)
               -> TOOL_MAP dispatch
               -> src/tools/article_tools.py
               -> src/tools/user_tools.py
               -> src/tools/menu_tools.py
               -> src/tools/tag_tools.py
               -> src/tools/redirect_tools.py
                    -> respektive src/services/*_service.py
                         -> Joomla 4 Core API

Extern MCP-klient
     -> /mcp (FastMCP mount i main.py)
          -> src/tools/article_tools.py etc.
               -> respektive src/services/*_service.py
                    -> Joomla 4 Core API
```

## Lagers ansvar

- **llm_service.py**: Beskriver tillgängliga verktyg enligt OpenAI function-calling-schema.
- **chat_router.py**: Orkestrerar flödet, hanterar bekräftelser och mappar verktygsnamn till rätt Python-funktion.
- **tools/\*\_tools.py**: Implementerar domänspecifika operationer (artiklar, användare, menyer etc.).
- **services/\*\_service.py**: Pratar direkt med Joomla 4 Core API.

## Lägga till ett nytt verktyg

1. Implementera funktionen i rätt `src/tools/*_tools.py`-fil.
2. Lägg till schema-entry i `OPENAI_TOOL_SCHEMAS` i `src/services/llm_service.py`.
3. Lägg till dispatch-entry i `TOOL_MAP` i `src/routes/chat_router.py`.
4. Om verktyget är destruktivt, lägg till namnet i `DESTRUCTIVE_TOOLS` i `chat_router.py`.

## Endpoints

| Metod | Endpoint | Syfte                                                                 |
| ----- | -------- | --------------------------------------------------------------------- |
| GET   | `/`      | Renderar chat-UI (index.html)                                         |
| POST  | `/chat`  | Tar emot prompt, låter LLM välja verktyg och utför Joomla-operationer |
| ASGI  | `/mcp`   | Exponerar verktyg för externa MCP-klienter                            |

## Logging

- Loggning konfigureras i `src/config/logging_config.py` och initieras från `main.py`.
- Känsliga fält maskeras innan loggning.
- Fel och händelser loggas för spårbarhet.

## Exempel på verktyg

- `get_articles` – Lista alla artiklar
- `get_article` – Hämta artikel med ID
- `create_article` – Skapa ny artikel
- `delete_article` – Ta bort artikel (kräver bekräftelse)
- `get_users`, `get_menus`, `get_tags`, `get_redirects` m.fl.

## Utveckling

- Projektet är modulärt och lätt att bygga ut med fler verktyg/domäner.
- Följ checklistan ovan för att lägga till nya funktioner.

## Projektstruktur

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
     │   ├── __init__.py
     │   ├── articles_service.py
     │   ├── joomla_service.py
     │   ├── llm_service.py
     │   ├── menus_service.py
     │   ├── redirects_service.py
     │   ├── tags_service.py
     │   └── users_service.py
     ├── tools/
     │   ├── article_tools.py
     │   ├── menu_tools.py
     │   ├── mcp_tools.py
     │   ├── redirect_tools.py
     │   ├── tag_tools.py
     │   └── user_tools.py
     └── utils/
          ├── config.py
          └── formatters.py
```

---

**Repo:** `kimpabooy/Joomla_MCP_Server`  
**Python:** `>= 3.13`
