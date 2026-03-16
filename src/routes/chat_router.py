import logging
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
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

router = APIRouter()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "cache_bust": datetime.now().timestamp()})


@router.post("/chat")
def chat(body: dict):
    """Ta emot naturligt språk, låt LLM välja rätt tool."""
    if "message" not in body:
        raise HTTPException(
            status_code=422,
            detail="Request body måste innehålla nyckeln 'message'.",
        )
    try:
        result = ask_llm(body["message"])
    except Exception as e:
        logger.error(f"LLM-fel: {e}")
        return {"response": f"AI-tjänsten är inte tillgänglig just nu: {type(e).__name__}"}

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
