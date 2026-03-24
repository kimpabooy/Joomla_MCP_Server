"""
Generella formatteringsfunktioner för Joomla MCP.
"""


def format_article_data(article: dict) -> dict:
    attributes = article.get("attributes", {})
    return {
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
    }
