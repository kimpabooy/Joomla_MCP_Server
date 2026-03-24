"""
This module defines the MCP tools that allow the LLM to interact with Joomla users.
"""

from src.utils.config import get_token, mcp
from src.services.users_service import (
    get_joomla_users,
    get_joomla_user,
    create_joomla_user,
    delete_joomla_user,
    edit_joomla_user
)


@mcp.tool()
def get_users() -> list[dict]:
    """Fetches all users from Joomla and returns a list of formatted user data."""
    users = get_joomla_users(get_token())
    return [{
            "id": user.get("id"),
            "name": user.get("attributes", {}).get("name"),
            "username": user.get("attributes", {}).get("username"),
            "email": user.get("attributes", {}).get("email"),
            } for user in users]


@mcp.tool()
def get_user(user_id: int) -> dict:
    """Fetches details for a specific user based on their ID."""
    user = get_joomla_user(get_token(), user_id)
    return {
        "id": user.get("id"),
        "name": user.get("attributes", {}).get("name"),
        "username": user.get("attributes", {}).get("username"),
        "email": user.get("attributes", {}).get("email")
    }


@mcp.tool()
def create_user(name: str, username: str, email: str, password: str) -> dict:
    """Creates a new user in Joomla with the given details."""
    try:
        result = create_joomla_user(
            get_token(), name, username, email, password)
        return {
            "id": result.get("id"),
            "name": result.get("attributes", {}).get("name"),
            "username": result.get("attributes", {}).get("username"),
            "email": result.get("attributes", {}).get("email")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_user(user_id: int) -> dict:
    """Deletes a user from Joomla based on their ID."""
    try:
        result = delete_joomla_user(get_token(), user_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_user(user_id: int, name: str, username: str, email: str) -> dict:
    """Edits an existing user in Joomla based on their ID. Only provided fields will be updated."""
    try:
        result = edit_joomla_user(get_token(), user_id, name, username, email)
        return {
            "id": result.get("id"),
            "name": result.get("attributes", {}).get("name"),
            "username": result.get("attributes", {}).get("username"),
            "email": result.get("attributes", {}).get("email")
        }
    except Exception as e:
        return {"error": str(e)}
