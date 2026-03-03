from pydantic import BaseModel
from src.services.joomla_service import get_joomla_articles, get_joomla_article, unpublish_joomla_article, publish_joomla_article, trash_joomla_article


class MCPRequest(BaseModel):
    tool: str
    arguments: dict | None = None


def get_all_endpoints(router):
    endpoints = []
    for route in router.routes:
        if hasattr(route, 'path') and route.path != "/mcp-proxy" and hasattr(route, 'methods'):
            endpoints.append({
                "name": getattr(route, 'name', None),
                "path": route.path,
                "methods": list(route.methods) if route.methods else []
            })
    return {"endpoints": endpoints}


def get_articles(JOOMLA_API_TOKEN: str):
    articles = get_joomla_articles(JOOMLA_API_TOKEN)

    articles_formatted = []
    for article in articles:
        attributes = article.get("attributes", {})
        articles_formatted.append({
            "id": article.get("id"),
            "title": attributes.get("title"),
            "alias": attributes.get("alias"),
            "state": attributes.get("state") == 1 and "[1] / Published"
            or (attributes.get("state") == 0 and "[0] / Unpublished"
                or (attributes.get("state") == -2 and "[-2] / Trashed"
                or "[Unknown]")),
            "created_by": attributes.get("created_by"),
            "created": attributes.get("created"),
            "last_modified": attributes.get("modified")
        })

    return MCPRequest(tool="get_articles", arguments={"articles": articles_formatted}).model_dump()


def get_article_id(JOOMLA_API_TOKEN: str, article_id: int):
    article = get_joomla_article(JOOMLA_API_TOKEN, article_id)
    return MCPRequest(tool="get_article_id", arguments={"article": article}).model_dump()


# //////////////////////////////////////////////////////////////////////////////////////
# Funktion för att avpublicera en artikel baserat på dess ID
# //////////////////////////////////////////////////////////////////////////////////////
def unpublish_article(JOOMLA_API_TOKEN: str, article_id: int):
    result = unpublish_joomla_article(JOOMLA_API_TOKEN, article_id)
    return MCPRequest(tool="unpublish_article", arguments={"article": result}).model_dump()


# //////////////////////////////////////////////////////////////////////////////////////
# Funktion för att publicera en artikel baserat på dess ID
# //////////////////////////////////////////////////////////////////////////////////////
def publish_article(JOOMLA_API_TOKEN: str, article_id: int):
    result = publish_joomla_article(JOOMLA_API_TOKEN, article_id)
    return MCPRequest(tool="publish_article", arguments={"article": result}).model_dump()


def trash_article(JOOMLA_API_TOKEN: str, article_id: int):
    result = trash_joomla_article(JOOMLA_API_TOKEN, article_id)
    return MCPRequest(tool="trash_article", arguments={"article": result}).model_dump()


def create_article(JOOMLA_API_TOKEN: str, title: str, content: str):
    pass


def delete_article(JOOMLA_API_TOKEN: str, article_id: int):
    pass


def edit_article(JOOMLA_API_TOKEN: str, article_id: int, title: str = None, content: str = None):
    pass


def view_article(JOOMLA_API_TOKEN: str, article_id: int):
    pass


def copy_article(JOOMLA_API_TOKEN: str, article_id: int):
    pass


def move_article(JOOMLA_API_TOKEN: str, article_id: int, new_category_id: int):
    pass


def feature_article(JOOMLA_API_TOKEN: str, article_id: int):
    pass


def unfeature_article(JOOMLA_API_TOKEN: str, article_id: int):
    pass


def archive_article(JOOMLA_API_TOKEN: str, article_id: int):
    pass


def unarchive_article(JOOMLA_API_TOKEN: str, article_id: int):
    pass


def check_article_status(JOOMLA_API_TOKEN: str, article_id: int):
    pass
