"""
This module defines the MCP tools that allow the LLM to interact with Joomla tags.
"""

from src.utils.config import get_token, mcp
from src.services.tags_service import (
    get_joomla_tags,
    get_joomla_tag,
    create_joomla_tag,
    edit_joomla_tag,
    delete_joomla_tag,
    get_joomla_tag_items,
    get_joomla_tag_item,
    create_joomla_tag_item,
    edit_joomla_tag_item,
    delete_joomla_tag_item
)


@mcp.tool()
def get_tags() -> list[dict]:
    """Fetches all tags from Joomla and returns a list of formatted tag data."""
    tags = get_joomla_tags(get_token())
    return [{
            "id": tag.get("id"),
            "title": tag.get("attributes", {}).get("title"),
            "alias": tag.get("attributes", {}).get("alias")
            } for tag in tags]


@mcp.tool()
def get_tag(tag_id: int) -> dict:
    """Fetches details for a specific tag based on its ID."""
    tag = get_joomla_tag(get_token(), tag_id)
    return {
        "id": tag.get("id"),
        "title": tag.get("attributes", {}).get("title"),
        "alias": tag.get("attributes", {}).get("alias")
    }


@mcp.tool()
def create_tag(title: str, alias: str) -> dict:
    """Creates a new tag in Joomla with the given title and alias."""
    try:
        result = create_joomla_tag(get_token(), title, alias)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "alias": result.get("attributes", {}).get("alias")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_tag(tag_id: int, title: str, alias: str) -> dict:
    """Edits an existing tag in Joomla based on its ID with new title and alias."""
    try:
        result = edit_joomla_tag(get_token(), tag_id, title, alias)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "alias": result.get("attributes", {}).get("alias")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_tag(tag_id: int) -> dict:
    """Deletes a tag from Joomla based on its ID."""
    try:
        result = delete_joomla_tag(get_token(), tag_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_tag_items(tag_id: int) -> list[dict]:
    """Fetches all items associated with a specific tag from Joomla and returns a list of formatted tag item data."""
    items = get_joomla_tag_items(get_token(), tag_id)
    return [{
            "id": item.get("id"),
            "type": item.get("attributes", {}).get("type"),
            "item_id": item.get("attributes", {}).get("item_id")
            } for item in items]


@mcp.tool()
def get_tag_item(tag_id: int, item_id: int) -> dict:
    """Fetches details for a specific tag item based on its ID and the tag it belongs to."""
    item = get_joomla_tag_item(get_token(), tag_id, item_id)
    return {
        "id": item.get("id"),
        "type": item.get("attributes", {}).get("type"),
        "item_id": item.get("attributes", {}).get("item_id")
    }


@mcp.tool()
def create_tag_item(tag_id: int, type: str, item_id: int) -> dict:
    """Creates a new tag item under a specific tag in Joomla."""
    try:
        result = create_joomla_tag_item(get_token(), tag_id, item_id)
        return {
            "id": result.get("id"),
            "type": result.get("attributes", {}).get("type"),
            "item_id": result.get("attributes", {}).get("item_id")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_tag_item(tag_id: int, item_id: int, type: str, new_item_id: int) -> dict:
    """Edits an existing tag item under a specific tag in Joomla."""
    try:
        result = edit_joomla_tag_item(
            get_token(), tag_id, item_id, new_item_id)
        return {
            "id": result.get("id"),
            "type": result.get("attributes", {}).get("type"),
            "item_id": result.get("attributes", {}).get("item_id")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_tag_item(tag_id: int, item_id: int) -> dict:
    """Deletes a tag item under a specific tag in Joomla."""
    try:
        result = delete_joomla_tag_item(get_token(), tag_id, item_id)
        return result
    except Exception as e:
        return {"error": str(e)}
