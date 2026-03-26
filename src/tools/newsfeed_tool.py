"""
This module defines the MCP tools that allow the LLM to interact with Joomla newsfeeds.
"""

from src.utils.config import get_token, mcp
from src.services.joomla_API import newsfeeds_service


@mcp.tool()
def get_newsfeeds() -> list[dict]:
    """Fetches all newsfeeds from Joomla and returns a list of formatted newsfeed data."""
    newsfeeds = newsfeeds_service.get_joomla_newsfeeds(get_token())
    return [{
            "id": newsfeed.get("id"),
            "title": newsfeed.get("attributes", {}).get("title"),
            "link": newsfeed.get("attributes", {}).get("link"),
            "published": newsfeed.get("attributes", {}).get("published") == 1
            # Limit to 100 newsfeeds to avoid overwhelming the response
            } for newsfeed in newsfeeds][:100]


@mcp.tool()
def get_newsfeed(newsfeed_id: int) -> dict:
    """Fetches details for a specific newsfeed based on its ID."""
    newsfeed = newsfeeds_service.get_joomla_newsfeed(get_token(), newsfeed_id)
    return {
        "id": newsfeed.get("id"),
        "title": newsfeed.get("attributes", {}).get("title"),
        "link": newsfeed.get("attributes", {}).get("link"),
        "published": newsfeed.get("attributes", {}).get("published") == 1
    }


@mcp.tool()
def create_newsfeed(title: str, link: str, published: bool) -> dict:
    """Creates a new newsfeed in Joomla with the given title, link, and published state."""
    try:
        result = newsfeeds_service.create_joomla_newsfeed(
            get_token(), title, link, published)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "link": result.get("attributes", {}).get("link"),
            "published": result.get("attributes", {}).get("published") == 1
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_newsfeed(newsfeed_id: int, title: str, link: str, published: bool) -> dict:
    """Edits an existing newsfeed in Joomla based on its ID."""
    try:
        result = newsfeeds_service.edit_joomla_newsfeed(
            get_token(), newsfeed_id, title, link, published)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "link": result.get("attributes", {}).get("link"),
            "published": result.get("attributes", {}).get("published") == 1
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_newsfeed(newsfeed_id: int) -> dict:
    """Deletes a newsfeed in Joomla based on its ID."""
    try:
        newsfeeds_service.delete_joomla_newsfeed(get_token(), newsfeed_id)
        return {"success": True, "message": f"Newsfeed with ID {newsfeed_id} deleted successfully."}
    except Exception as e:
        return {"error": str(e)}
