"""
This module defines the MCP tools that allow the LLM to interact with Joomla languages.
"""

from src.utils.config import get_token, mcp
from src.services.joomla_API import languages_service


@mcp.tool()
def get_languages() -> list[dict]:
    """Fetches all languages from Joomla and returns a list of formatted language data."""
    languages = languages_service.get_joomla_languages(get_token())
    return [{
            "id": language.get("id"),
            "title": language.get("attributes", {}).get("title"),
            "code": language.get("attributes", {}).get("code"),
            "image": language.get("attributes", {}).get("image")
            } for language in languages]


@mcp.tool()
def get_language(language_id: int) -> dict:
    """Fetches details for a specific language based on its ID."""
    language = languages_service.get_joomla_language(get_token(), language_id)
    return {
        "id": language.get("id"),
        "title": language.get("attributes", {}).get("title"),
        "code": language.get("attributes", {}).get("code"),
        "image": language.get("attributes", {}).get("image")
    }


@mcp.tool()
def create_language(language_id: int, title: str, code: str, image: str, published: bool) -> dict:
    """Creates a new language in Joomla with the given title, code, and image."""
    try:
        result = languages_service.create_joomla_language(
            get_token(), title, code, image, published)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "code": result.get("attributes", {}).get("code"),
            "image": result.get("attributes", {}).get("image"),
            "published": result.get("attributes", {}).get("published")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_language(language_id: int, title: str, code: str, image: str, published: bool) -> dict:
    """Edits an existing language in Joomla based on its ID."""
    try:
        result = languages_service.edit_joomla_language(
            get_token(), language_id, title, code, image, published)
        return {
            "id": result.get("id"),
            "title": result.get("attributes", {}).get("title"),
            "code": result.get("attributes", {}).get("code"),
            "image": result.get("attributes", {}).get("image"),
            "published": result.get("attributes", {}).get("published")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_language(language_id: int) -> dict:
    """Deletes a language from Joomla based on its ID."""
    try:
        languages_service.delete_joomla_language(get_token(), language_id)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
