"""
This module defines the MCP tools that allow the LLM to interact with Joomla modules.
"""

from src.utils.config import get_token, mcp
from src.services.joomla_API import modules_service


@mcp.tool()
def get_modules() -> list[dict]:
    """Fetches all modules from Joomla and returns a list of formatted module data."""
    modules = modules_service.get_joomla_modules(get_token())
    return [{
            "id": module.get("id"),
            "title": module.get("attributes", {}).get("title"),
            "position": module.get("attributes", {}).get("position"),
            "published": module.get("attributes", {}).get("published") == 1
            } for module in modules]


@mcp.tool()
def get_module(module_id: int) -> dict:
    """Fetches details for a specific module based on its ID."""
    module = modules_service.get_joomla_module(get_token(), module_id)
    return {
        "id": module.get("id"),
        "title": module.get("attributes", {}).get("title"),
        "position": module.get("attributes", {}).get("position"),
        "published": module.get("attributes", {}).get("published") == 1
    }


@mcp.tool()
def create_module(title: str, position: str, published: bool) -> dict:
    """Creates a new module in Joomla with the given title, position, and published state."""
    try:
        result = modules_service.create_joomla_module(
            get_token(), title, position, published)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "position": result.get("attributes", {}).get("position"),
            "published": result.get("attributes", {}).get("published") == 1
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_module(module_id: int, title: str, position: str, published: bool) -> dict:
    """Edits an existing module in Joomla based on its ID."""
    try:
        result = modules_service.edit_joomla_module(
            get_token(), module_id, title, position, published)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "position": result.get("attributes", {}).get("position"),
            "published": result.get("attributes", {}).get("published") == 1
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_module(module_id: int) -> dict:
    """Deletes an existing module in Joomla based on its ID."""
    try:
        modules_service.delete_joomla_module(get_token(), module_id)
        return {"message": f"Module with ID {module_id} has been deleted."}
    except Exception as e:
        return {"error": str(e)}
