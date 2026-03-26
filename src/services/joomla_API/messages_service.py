"""
Service functions for Joomla messages.
"""

from src.utils.config import JOOMLA_URL, get_headers
from typing import Any, Dict, List
import requests


def get_joomla_messages(token: str) -> List[Dict[str, Any]]:
    """Fetches all messages from Joomla and returns a list of formatted message data."""
    url = f"{JOOMLA_URL}/messages"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_message(token: str, message_id: int) -> Dict[str, Any]:
    """Fetches details for a specific message based on its ID."""
    url = f"{JOOMLA_URL}/messages/{message_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_message(token: str, name: str, email: str, subject: str, body: str) -> Dict[str, Any]:
    """Creates a new message in Joomla with the given subject and body."""
    url = f"{JOOMLA_URL}/messages"
    headers = get_headers(token)
    data = {
        "name": name,
        "email": email,
        "subject": subject,
        "body": body
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_message(token: str, message_id: int, name: str, email: str, subject: str, body: str) -> Dict[str, Any]:
    """Edits an existing message in Joomla based on its ID."""
    url = f"{JOOMLA_URL}/messages/{message_id}"
    headers = get_headers(token)
    data = {
        "name": name,
        "email": email,
        "subject": subject,
        "body": body
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_message(token: str, message_id: int) -> Dict[str, Any]:
    """Deletes a message from Joomla based on its ID."""
    url = f"{JOOMLA_URL}/messages/{message_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if response.status_code == 404:
        raise Exception(f"Message with ID {message_id} not found.")

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return {"message": "Message deleted successfully."}
