"""
This module defines the MCP tools that allow the LLM to interact with Joomla messages.
"""

from src.utils.config import get_token, mcp
from src.services.joomla_API import messages_service


@mcp.tool()
def get_messages() -> list[dict]:
    """Fetches all messages from Joomla and returns a list of formatted message data."""
    messages = messages_service.get_joomla_messages(get_token())
    return [{
            "id": message.get("id"),
            "name": message.get("attributes", {}).get("name"),
            "email": message.get("attributes", {}).get("email"),
            "subject": message.get("attributes", {}).get("subject"),
            "message": message.get("attributes", {}).get("message")
            # Limit to 100 messages for performance
            } for message in messages][:100]


@mcp.tool()
def get_message(message_id: int) -> dict:
    """Fetches details for a specific message based on its ID."""
    message = messages_service.get_joomla_message(get_token(), message_id)
    return {
        "id": message.get("id"),
        "name": message.get("attributes", {}).get("name"),
        "email": message.get("attributes", {}).get("email"),
        "subject": message.get("attributes", {}).get("subject"),
        "message": message.get("attributes", {}).get("message")
    }


@mcp.tool()
def create_message(name: str, email: str, subject: str, message: str) -> dict:
    """Creates a new message in Joomla with the given details."""
    try:
        result = messages_service.create_joomla_message(
            get_token(), name, email, subject, message)
        return {
            "id": result.get("id"),
            "name": result.get("attributes", {}).get("name"),
            "email": result.get("attributes", {}).get("email"),
            "subject": result.get("attributes", {}).get("subject"),
            "message": result.get("attributes", {}).get("message")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_message(message_id: int, name: str, email: str, subject: str, message: str) -> dict:
    """Edits an existing message in Joomla based on its ID."""
    try:
        result = messages_service.edit_joomla_message(
            get_token(), message_id, name, email, subject, message)
        return {
            "id": result.get("id"),
            "name": result.get("attributes", {}).get("name"),
            "email": result.get("attributes", {}).get("email"),
            "subject": result.get("attributes", {}).get("subject"),
            "message": result.get("attributes", {}).get("message")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_message(message_id: int) -> dict:
    """Deletes a message from Joomla based on its ID."""
    try:
        messages_service.delete_joomla_message(get_token(), message_id)
        return {"message": "Message deleted successfully."}
    except Exception as e:
        return {"error": str(e)}
