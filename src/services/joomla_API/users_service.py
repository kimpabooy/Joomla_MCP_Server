"""
Service functions for Joomla users.
"""

import requests
import os
from src.utils.config import get_headers
from typing import Any, Dict, List
JOOMLA_API_URL = os.getenv("JOOMLA_API_URL")


def get_joomla_users(token: str) -> List[Dict[str, Any]]:
    """Fetches all users from Joomla and returns a list of formatted user data."""
    url = f"{JOOMLA_API_URL}/users"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_user(token: str, user_id: int) -> Dict[str, Any]:
    """Fetches details for a specific user based on their ID."""
    url = f"{JOOMLA_API_URL}/users/{user_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_user(token: str, name: str, username: str, email: str, password: str) -> Dict[str, Any]:
    """Creates a new user in Joomla with the given details."""
    url = f"{JOOMLA_API_URL}/users"
    headers = get_headers(token)
    data = {
        "name": name,
        "username": username,
        "email": email,
        "password": password,
        "groups": [2]  # Default to Registered group
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_user(token: str, user_id: int) -> Dict[str, Any]:
    """Deletes a user from Joomla based on their ID."""
    url = f"{JOOMLA_API_URL}/users/{user_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if response.status_code == 404:
        raise Exception(f"User with ID {user_id} not found.")

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return {
        "message": f"User {user_id} has been deleted.",
    }


def edit_joomla_user(token: str, user_id: int, name: str, username: str, email: str) -> Dict[str, Any]:
    """Edits an existing user in Joomla based on their ID."""
    url = f"{JOOMLA_API_URL}/users/{user_id}"
    headers = get_headers(token)
    data = {
        "name": name,
        "username": username,
        "email": email
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})
