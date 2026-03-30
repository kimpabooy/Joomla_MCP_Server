"""
This module defines the MCP tools that allow the LLM to interact with Joomla categories.
"""

from src.utils.config import get_token, mcp
from src.utils.formatters import format_article_data as _format_article_data
from src.services.joomla_API import categories_service


@mcp.tool()
def get_categories() -> list[dict]:
    """Fetches all categories from Joomla and returns a list of formatted category data."""
    categories = categories_service.get_joomla_categories(get_token())
    return [_format_article_data(category) for category in categories]


@mcp.tool()
def get_category(category_id: int) -> dict:
    """Fetches details for a specific category based on its ID."""
    category = categories_service.get_joomla_category(get_token(), category_id)
    return _format_article_data(category)


@mcp.tool()
def create_category(title: str, parent_id: int, published: bool) -> dict:
    """Creates a new category in Joomla with the given title, parent ID, and published state."""
    try:
        result = categories_service.create_joomla_category(
            get_token(), title, parent_id, published)
        return _format_article_data(result)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_category(category_id: int, title: str, parent_id: int, published: bool) -> dict:
    """Edits an existing category in Joomla based on its ID."""
    try:
        result = categories_service.edit_joomla_category(
            get_token(), category_id, title, parent_id, published)
        return _format_article_data(result)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_category(category_id: int) -> dict:
    """Deletes a category in Joomla based on its ID."""
    try:
        result = categories_service.delete_joomla_category(
            get_token(), category_id)
        return {"success": True, "message": f"Category {category_id} deleted successfully."}
    except Exception as e:
        return {"error": str(e)}
