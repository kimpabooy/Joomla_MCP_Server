"""
Service functions for Joomla modules.
"""

from src.utils.config import JOOMLA_URL, get_headers
from typing import Any, Dict, List
import requests


def get_joomla_modules(token: str) -> List[Dict[str, Any]]:
    """Fetches all modules from Joomla and returns a list of formatted module data."""
    url = f"{JOOMLA_URL}/modules"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_module(token: str, module_id: int) -> Dict[str, Any]:
    """Fetches details for a specific module based on its ID."""
    url = f"{JOOMLA_URL}/modules/{module_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_module(token: str, title: str, position: str, published: bool) -> Dict[str, Any]:
    """Creates a new module in Joomla with the given title, position, and published state."""
    url = f"{JOOMLA_URL}/modules"
    headers = get_headers(token)
    data = {
        "title": title,
        "position": position,
        "published": published
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_module(token: str, module_id: int, title: str, position: str, published: bool) -> Dict[str, Any]:
    """Edits an existing module in Joomla based on its ID."""
    url = f"{JOOMLA_URL}/modules/{module_id}"
    headers = get_headers(token)
    data = {
        "title": title,
        "position": position,
        "published": published
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_module(token: str, module_id: int) -> None:
    """Deletes a module in Joomla based on its ID."""
    url = f"{JOOMLA_URL}/modules/{module_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
