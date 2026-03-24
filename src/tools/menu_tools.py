"""
This module defines the MCP tools that allow the LLM to interact with Joomla menus.
"""

from src.utils.config import get_token, mcp
from src.services.menus_service import (
    get_joomla_menus,
    get_joomla_menu,
    create_joomla_menu,
    edit_joomla_menu,
    delete_joomla_menu,
    get_joomla_menu_items,
    get_joomla_menu_item,
    create_joomla_menu_item,
    edit_joomla_menu_item,
    delete_joomla_menu_item
)


@mcp.tool()
def get_menus() -> list[dict]:
    """Fetches all menus from Joomla and returns a list of formatted menu data."""
    menus = get_joomla_menus(get_token())
    return [{
            "id": menu.get("id"),
            "title": menu.get("attributes", {}).get("title"),
            "alias": menu.get("attributes", {}).get("alias")
            } for menu in menus]


@mcp.tool()
def get_menu(menu_id: int) -> dict:
    """Fetches details for a specific menu based on its ID."""
    menu = get_joomla_menu(get_token(), menu_id)
    return {
        "id": menu.get("id"),
        "title": menu.get("attributes", {}).get("title"),
        "alias": menu.get("attributes", {}).get("alias")
    }


@mcp.tool()
def create_menu(title: str, alias: str) -> dict:
    """Creates a new menu in Joomla with the given title and alias."""
    try:
        result = create_joomla_menu(get_token(), title, alias)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "alias": result.get("attributes", {}).get("alias")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_menu(menu_id: int, title: str, alias: str) -> dict:
    """Edits an existing menu in Joomla based on its ID with new title and alias."""
    try:
        result = edit_joomla_menu(get_token(), menu_id, title, alias)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "alias": result.get("attributes", {}).get("alias")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_menu(menu_id: int) -> dict:
    """Deletes a menu from Joomla based on its ID."""
    try:
        result = delete_joomla_menu(get_token(), menu_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_menu_items(menu_id: int) -> list[dict]:
    """Fetches all menu items for a specific menu from Joomla and returns a list of formatted menu item data."""
    items = get_joomla_menu_items(get_token(), menu_id)
    return [{
            "id": item.get("id"),
            "title": item.get("attributes", {}).get("title"),
            "alias": item.get("attributes", {}).get("alias"),
            "link": item.get("attributes", {}).get("link")
            } for item in items]


@mcp.tool()
def get_menu_item(menu_id: int, item_id: int) -> dict:
    """Fetches details for a specific menu item based on its ID and the menu it belongs to."""
    item = get_joomla_menu_item(get_token(), menu_id, item_id)
    return {
        "id": item.get("id"),
        "title": item.get("attributes", {}).get("title"),
        "alias": item.get("attributes", {}).get("alias"),
        "link": item.get("attributes", {}).get("link")
    }


@mcp.tool()
def create_menu_item(menu_id: int, title: str, alias: str, link: str) -> dict:
    """Creates a new menu item under a specific menu in Joomla."""
    try:
        result = create_joomla_menu_item(
            get_token(), menu_id, title, alias, link)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "alias": result.get("attributes", {}).get("alias"),
            "link": result.get("attributes", {}).get("link")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_menu_item(menu_id: int, item_id: int, title: str, alias: str, link: str) -> dict:
    """Edits an existing menu item under a specific menu in Joomla."""
    try:
        result = edit_joomla_menu_item(
            get_token(), menu_id, item_id, title, alias, link)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "alias": result.get("attributes", {}).get("alias"),
            "link": result.get("attributes", {}).get("link")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_menu_item(menu_id: int, item_id: int) -> dict:
    """Deletes a menu item under a specific menu in Joomla."""
    try:
        result = delete_joomla_menu_item(get_token(), menu_id, item_id)
        return result
    except Exception as e:
        return {"error": str(e)}
