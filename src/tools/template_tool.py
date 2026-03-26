"""
This module defines the MCP tools that allow the LLM to interact with Joomla templates.
"""

from src.utils.config import get_token, mcp
from src.services.joomla_API import templates_service


@mcp.tool()
def get_templates() -> list[dict]:
    """Fetches all templates from Joomla and returns a list of formatted template data."""
    templates = templates_service.get_joomla_templates(get_token())
    return [{
            "id": template.get("id"),
            "name": template.get("attributes", {}).get("name"),
            "client_id": template.get("attributes", {}).get("client_id"),
            "home": template.get("attributes", {}).get("home") == 1
            } for template in templates]


@mcp.tool()
def get_template(template_id: int) -> dict:
    """Fetches details for a specific template based on its ID."""
    template = templates_service.get_joomla_template(get_token(), template_id)
    return {
        "id": template.get("id"),
        "name": template.get("attributes", {}).get("name"),
        "client_id": template.get("attributes", {}).get("client_id"),
        "home": template.get("attributes", {}).get("home") == 1
    }


@mcp.tool()
def create_template(name: str, client_id: int, home: bool) -> dict:
    """Creates a new template in Joomla with the given name, client ID, and home state."""
    try:
        result = templates_service.create_joomla_template(
            get_token(), name, client_id, home)
        return {
            "id": result.get("id"),
            "name": result.get("attributes", {}).get("name"),
            "client_id": result.get("attributes", {}).get("client_id"),
            "home": result.get("attributes", {}).get("home") == 1
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_template(template_id: int, name: str, client_id: int, home: bool) -> dict:
    """Edits an existing template in Joomla based on its ID."""
    try:
        result = templates_service.edit_joomla_template(
            get_token(), template_id, name, client_id, home)
        return {
            "id": result.get("id"),
            "name": result.get("attributes", {}).get("name"),
            "client_id": result.get("attributes", {}).get("client_id"),
            "home": result.get("attributes", {}).get("home") == 1
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_template(template_id: int) -> dict:
    """Deletes a template from Joomla based on its ID."""
    try:
        result = templates_service.delete_joomla_template(
            get_token(), template_id)
        return result
    except Exception as e:
        return {"error": str(e)}
