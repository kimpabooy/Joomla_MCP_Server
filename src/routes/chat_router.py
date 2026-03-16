import logging
import time
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from src.services.llm_service import ask_llm
from src.tools.mcp_tools import (
    list_articles,
    get_article,
    publish,
    unpublish,
    trash,
    create_article,
    edit_article,
    remove_article,
)

"""
This module defines the FastAPI router for handling chat interactions.
The chat endpoint uses server-side guardrails to ensure that any tool calls that can mutate or delete content require explicit confirmation.
The module also maintains a temporary in-memory store for pending confirmations, which are cleaned up after a certain expiration time.
"""

router = APIRouter()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")

# Add more tool names here that need confirmation before execution.
DESTRUCTIVE_TOOLS = {"remove_article"}
CONFIRMATION_TTL_SECONDS = 300
PENDING_CONFIRMATIONS: dict[str, dict] = {}


def _cleanup_expired_confirmations() -> None:
    """Cleans up expired confirmations from PENDING_CONFIRMATIONS."""
    now = time.time()
    expired = [
        key
        for key, value in PENDING_CONFIRMATIONS.items()
        if value.get("expires_at", 0) < now
    ]
    for key in expired:
        PENDING_CONFIRMATIONS.pop(key, None)


@router.get("/")
def root(request: Request):
    """Renders the homepage."""
    return templates.TemplateResponse("index.html", {"request": request, "cache_bust": datetime.now().timestamp()})


@router.post("/chat")
def chat(body: dict):
    """Receives natural language input, lets the LLM choose the right tool with server-side guardrails."""
    _cleanup_expired_confirmations()
    message = body.get("message", "")

    # Explicit second step: execute only if a valid server-issued confirmation id is provided.
    if body.get("confirm") is True:
        confirmation_id = body.get("confirmation_id")
        if not confirmation_id:
            return {"error": "Bekräftelse saknar confirmation_id."}

        pending = PENDING_CONFIRMATIONS.pop(confirmation_id, None)
        if not pending:
            return {"error": "Ogiltig eller utgången bekräftelse."}

        result = {"tool": pending["tool"], "args": pending["args"]}
    else:
        if not isinstance(message, str) or not message.strip():
            return {"error": "Meddelande saknas."}

        # The LLM should ideally return a structured response indicating which tool to use and with what arguments.
        # Main logic: If the LLM suggests a tool that is in DESTRUCTIVE_TOOLS, we require an explicit confirmation step before executing it.
        # This adds a layer of safety for actions that can mutate or delete content.
        try:
            result = ask_llm(message)
        except Exception as e:
            logger.error(f"LLM-fel: {e}")
            return {"response": f"AI-tjänsten är inte tillgänglig just nu: {type(e).__name__}"}

        if "tool" in result and result["tool"] in DESTRUCTIVE_TOOLS:
            confirmation_id = str(uuid4())
            PENDING_CONFIRMATIONS[confirmation_id] = {
                "tool": result["tool"],
                "args": result["args"],
                "expires_at": time.time() + CONFIRMATION_TTL_SECONDS,
            }
            return {
                "requires_confirmation": True,
                "confirmation_id": confirmation_id,
                "proposed_action": {
                    "tool": result["tool"],
                    "args": result["args"],
                },
                "response": "Den här åtgärden är destruktiv och kräver bekräftelse. Vill du fortsätta?",
            }

        # if the LLM response doesn't require confirmation, we can execute it directly and return the result.
    if "tool" in result:
        tool_map = {
            "list_articles": lambda args: list_articles(),
            "get_article": lambda args: get_article(**args),
            "publish": lambda args: publish(**args),
            "unpublish": lambda args: unpublish(**args),
            "trash": lambda args: trash(**args),
            "create_article": lambda args: create_article(**args),
            "edit_article": lambda args: edit_article(**args),
            "remove_article": lambda args: remove_article(**args),
        }
        handler = tool_map.get(result["tool"])
        if handler:
            return handler(result["args"])
        return {"error": f"Okänt verktyg: {result['tool']}"}

    return {"response": result["text"]}
