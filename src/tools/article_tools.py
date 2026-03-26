"""
This module defines the MCP tools that allow the LLM to interact with Joomla articles.
"""

from src.utils.config import get_token, mcp
from src.utils.formatters import format_article_data as _format_article_data
from src.services.joomla_API import articles_service


@mcp.tool()
def get_articles() -> list[dict]:
    """Fetches all articles from Joomla and returns a list of formatted article data."""
    articles = articles_service.get_joomla_articles(get_token())
    return [_format_article_data(article) for article in articles]


@mcp.tool()
def get_article(article_id: int) -> dict:
    """Fetches details for a specific article based on its ID."""
    article = articles_service.get_joomla_article(get_token(), article_id)
    return _format_article_data(article)


@mcp.tool()
def publish_article(article_id: int) -> dict:
    """Publishes an article based on its ID."""
    result = articles_service.publish_joomla_article(get_token(), article_id)
    return _format_article_data(result)


@mcp.tool()
def unpublish_article(article_id: int) -> dict:
    """Unpublishes an article based on its ID."""
    result = articles_service.unpublish_joomla_article(get_token(), article_id)
    return _format_article_data(result)


@mcp.tool()
def trash_article(article_id: int) -> dict:
    """Trashes an article based on its ID."""
    result = articles_service.trash_joomla_article(get_token(), article_id)
    return _format_article_data(result)


@mcp.tool()
def get_unpublished_articles() -> list[dict]:
    """Fetches all unpublished articles from Joomla."""
    articles = articles_service.get_unpublished_joomla_articles(get_token())
    return [_format_article_data(article) for article in articles]


@mcp.tool()
def create_article(title: str, content: str) -> dict:
    """Creates a new article with the given title and content."""
    try:
        result = articles_service.create_joomla_article(
            get_token(), title, content)
        return _format_article_data(result)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_article(article_id: int) -> dict:
    """Permanently deletes an article based on its ID."""
    try:
        result = articles_service.delete_joomla_article(
            get_token(), article_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_article(article_id: int, title: str, content: str) -> dict:
    """Edits an existing article based on its ID with new title and content. Alias updates automatically."""
    try:
        result = articles_service.edit_joomla_article(
            get_token(), article_id, title, content)
        return _format_article_data(result)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def copy_article(article_id: int, new_title: str) -> dict:
    """Creates a copy of an existing article based on its ID. The new article will have the provided title and the same content as the original."""
    try:
        result = articles_service.copy_joomla_article(
            get_token(), article_id, new_title)
        return _format_article_data(result)
    except Exception as e:
        return {"error": str(e)}
