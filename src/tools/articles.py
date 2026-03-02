from pydantic import BaseModel
from src.services.joomla_service import get_joomla_articles


class MCPRequest(BaseModel):  # JSON-serialiserbar modell för att representera ett verktygsanrop
    tool: str
    arguments: dict | None = None


# //////////////////////////////////////////////////////////////////////////////////////
# Verktyg för att hämta artiklar från Joomla API och lista alla endpoints
# //////////////////////////////////////////////////////////////////////////////////////
def get_all_endpoints(router):
    return {
        "endpoints": [
            {
                "name": getattr(route, 'name', None),
                "path": route.path,
                "methods": list(route.methods),
                # "summary": getattr(route, 'summary', None),
                # "description": getattr(route, 'description', None),
            }
            for route in router.routes
            if hasattr(route, 'path') and hasattr(route, 'methods')
        ]
    }


# //////////////////////////////////////////////////////////////////////////////////////
# Funktion för att hämta alla artiklar från Joomla API
# //////////////////////////////////////////////////////////////////////////////////////
def get_articles(JOOMLA_API_TOKEN: str):
    articles = get_joomla_articles(JOOMLA_API_TOKEN)

    articles_formatted = []
    for article in articles:
        attributes = article.get("attributes", {})
        articles_formatted.append({
            "id": article.get("id"),
            "title": attributes.get("title"),
            "alias": attributes.get("alias"),
            # om state är 1 så är artikeln public,
            # om state är 0 så är artikeln unpublished,
            # om state är -2 så är artikeln trashed

            "state": attributes.get("state") == 1 and "[1] / Published"
            or (attributes.get("state") == 0 and "[0] / Unpublished"
                or (attributes.get("state") == -2 and "[-2] / Trashed"
                    or "[Unknown]")),
            # "state": attributes.get("state"),
            "created_by": attributes.get("created_by"),
            "created": attributes.get("created"),
            "last_modified": attributes.get("modified")
            # Lägg till fler fält efter behov...
        })

    return MCPRequest(tool="get_articles", arguments={"articles": articles_formatted, }).model_dump()
    # return MCPRequest(tool="get_articles", arguments={"articles": articles}).model_dump()
