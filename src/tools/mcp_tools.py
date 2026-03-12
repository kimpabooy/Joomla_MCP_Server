from fastmcp import FastMCP
from os import getenv
from src.services.joomla_service import (
    create_joomla_article,
    get_joomla_articles,
    get_joomla_article,
    publish_joomla_article,
    unpublish_joomla_article,
    trash_joomla_article,
    remove_joomla_article,
    edit_joomla_article,
)

# Create the FastMCP server instance
mcp = FastMCP("Joomla MCP Server")


def get_token() -> str:
    token = getenv("JOOMLA_API_TOKEN")
    if not token:
        raise ValueError("JOOMLA_API_TOKEN saknas i miljövariabler!")
    return token


# Helper function to format article data into a more readable structure
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


""""
Defines MCP tools corresponding to the various Joomla article operations.
Each tool is decorated with @mcp.tool() and has a clear docstring describing its functionality
Each tool calls the corresponding function in joomla_service and formats the result before returning it.
"""


@mcp.tool()
def list_articles() -> list[dict]:
    """Fetches all articles from Joomla and returns a list of formatted article data."""
    articles = get_joomla_articles(get_token())
    return [format_article_data(article) for article in articles]


@mcp.tool()
def get_article(article_id: int) -> dict:
    """Fetches details for a specific article based on its ID."""
    article = get_joomla_article(get_token(), article_id)
    return format_article_data(article)


@mcp.tool()
def publish(article_id: int) -> dict:
    """Publishes an article based on its ID."""
    result = publish_joomla_article(get_token(), article_id)
    return format_article_data(result)


@mcp.tool()
def unpublish(article_id: int) -> dict:
    """Unpublishes an article based on its ID."""
    result = unpublish_joomla_article(get_token(), article_id)
    return format_article_data(result)


@mcp.tool()
def trash(article_id: int) -> dict:
    """Trashes an article based on its ID."""
    result = trash_joomla_article(get_token(), article_id)
    return format_article_data(result)


@mcp.tool()
def create_article(title: str, content: str) -> dict:
    """Creates a new article with the given title and content."""
    try:
        result = create_joomla_article(get_token(), title, content)
        return format_article_data(result)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def remove_article(article_id: int) -> dict:
    """Permanently deletes an article based on its ID."""
    try:
        result = remove_joomla_article(get_token(), article_id)
        return format_article_data(result)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_article(article_id: int, title: str, content: str) -> dict:
    """Edits an existing article based on its ID with new title and content. Alias updates automatically."""
    try:
        result = edit_joomla_article(get_token(), article_id, title, content)
        return format_article_data(result)
    except Exception as e:
        return {"error": str(e)}
