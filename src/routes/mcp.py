import logging
from fastapi import APIRouter
from re import match
from src.tools.mcp_server import (
    list_articles,
    get_article,
    publish,
    unpublish,
    trash,
    create_article,
    remove_article,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def handle_help(_):
    return help_endpoints()


def handle_list_articles(_):
    return list_articles()


def handle_get_article(regex_match):
    article_id = int(regex_match.group(1))
    return get_article(article_id)


def handle_publish(regex_match):
    article_id = int(regex_match.group(1))
    return publish(article_id)


def handle_unpublish(regex_match):
    article_id = int(regex_match.group(1))
    return unpublish(article_id)


def handle_trash(regex_match):
    article_id = int(regex_match.group(1))
    return trash(article_id)


def handle_create_article(regex_match):
    # Förväntar sig att regex_match innehåller title och content i grupperna
    title = regex_match.group(1)
    content = regex_match.group(2)
    return create_article(title, content)


def handle_remove_article(regex_match):
    article_id = int(regex_match.group(1))
    return remove_article(article_id)


"""
Mappar endpoint-mönster (från chat-UI:t) till MCP tool-funktioner.
"name" är ett identifierande namn för verktyget.
"endpoint" är den beskrivande strängen som visas i hjälpkommandot.
"pattern" är en regex-sträng som används för att matcha inkommande endpoint-förfrågningar.
"handler" är en funktion som tar regex-match-objektet och anropar rätt MCP tool med nödvändiga argument.
"""
ENDPOINT_TOOL_MAP = [
    {
        "name": "list_articles",
        "endpoint": "/articles",
        "pattern": r"^/articles$",
        "description": "Lista alla artiklar",
        "handler": handle_list_articles
    },
    {
        "name": "get_article",
        "endpoint": "/articles/{id}",
        "pattern": r"^/articles/(\d+)$",
        "description": "Visa en specifik artikel",
        "handler": handle_get_article
    },
    {
        "name": "publish",
        "endpoint": "/articles/{id}/publish",
        "pattern": r"^/articles/(\d+)/publish$",
        "description": "Publicera en artikel",
        "handler": handle_publish
    },
    {
        "name": "unpublish",
        "endpoint": "/articles/{id}/unpublish",
        "pattern": r"^/articles/(\d+)/unpublish$",
        "description": "Avpublicera en artikel",
        "handler": handle_unpublish
    },
    {
        "name": "trash",
        "endpoint": "/articles/{id}/trash",
        "pattern": r"^/articles/(\d+)/trash$",
        "description": "Slänger (trashar) en artikel",
        "handler": handle_trash
    },
    {
        "name": "help",
        "endpoint": "/help",
        "pattern": r"^/help$",
        "description": "Visa hjälpinformation",
        "handler": handle_help
    },
    {
        "name": "create_article",
        "endpoint": "/articles/create",
        "pattern": r"^/articles/create\s+title:(.+)\s+content:(.+)$",
        "description": "Skapa en ny artikel med titel och innehåll",
        "handler": handle_create_article
    },
    {
        "name": "remove_article",
        "endpoint": "/articles/{id}/remove",
        "pattern": r"^/articles/(\d+)/remove$",
        "description": "Ta bort en artikel permanent",
        "handler": handle_remove_article
    }

]


@router.get("/mcp-proxy")
def mcp_proxy(endpoint: str):
    """Recieve endpoint string from chat UI and route to the correct MCP tool function."""
    logger.info(f"Requested endpoint: {endpoint}")

    for tool in ENDPOINT_TOOL_MAP:
        regex_match = match(tool["pattern"], endpoint)
        if regex_match:
            logger.info(f"Matching tool: {tool['name']}")
            return tool["handler"](regex_match)

    logger.warning(f"Ingen matchning för endpoint: {endpoint}")
    return {"error": f"Okänd endpoint: {endpoint}"}


@router.get("/help")
def help_endpoints():
    """Returns available endpoints for the chat UI, dynamically from ENDPOINT_TOOL_MAP."""
    return {
        "tools": [
            {"name": t["name"], "endpoint": t["endpoint"],
                "description": t["description"]}
            for t in ENDPOINT_TOOL_MAP
        ]
    }
