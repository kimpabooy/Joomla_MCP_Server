"""
This module defines the MCP tools that allow the LLM to interact with Joomla redirects.
"""

from src.utils.config import get_token, mcp
from src.services.joomla_API import redirects_service


@mcp.tool()
def get_redirects() -> list[dict]:
    """Fetches all redirects from Joomla and returns a list of formatted redirect data."""
    redirects = redirects_service.get_joomla_redirects(get_token())
    return [{
            "id": redirect.get("id"),
            "source": redirect.get("attributes", {}).get("source"),
            "destination": redirect.get("attributes", {}).get("destination")
            } for redirect in redirects]


@mcp.tool()
def get_redirect(redirect_id: int) -> dict:
    """Fetches details for a specific redirect based on its ID."""
    redirect = redirects_service.get_joomla_redirect(get_token(), redirect_id)
    return {
        "id": redirect.get("id"),
        "source": redirect.get("attributes", {}).get("source"),
        "destination": redirect.get("attributes", {}).get("destination")
    }


@mcp.tool()
def create_redirect(source: str, destination: str) -> dict:
    """Creates a new redirect in Joomla with the given source and destination."""
    try:
        result = redirects_service.create_joomla_redirect(
            get_token(), source, destination)
        return {
            "id": result.get("id"),
            "source": result.get("attributes", {}).get("source"),
            "destination": result.get("attributes", {}).get("destination")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_redirect(redirect_id: int, source: str, destination: str) -> dict:
    """Edits an existing redirect in Joomla based on its ID with new source and destination."""
    try:
        result = redirects_service.edit_joomla_redirect(
            get_token(), redirect_id, source, destination)
        return {
            "id": result.get("id"),
            "source": result.get("attributes", {}).get("source"),
            "destination": result.get("attributes", {}).get("destination")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_redirect(redirect_id: int) -> dict:
    """Deletes a redirect in Joomla based on its ID."""
    try:
        result = redirects_service.delete_joomla_redirect(
            get_token(), redirect_id)
        return result
    except Exception as e:
        return {"error": str(e)}
