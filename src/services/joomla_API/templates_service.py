"""
Service functions for Joomla templates.
"""

import requests
from src.utils.config import get_headers, get_joomla_api_url
from typing import Any, Dict, List

JOOMLA_API_URL = get_joomla_api_url()


def get_joomla_templates(token: str) -> List[Dict[str, Any]]:
    """Fetches all templates from Joomla and returns a list of formatted template data."""
    url = f"{JOOMLA_API_URL}/templates"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_template(token: str, template_id: int) -> Dict[str, Any]:
    """Fetches details for a specific template based on its ID."""
    url = f"{JOOMLA_API_URL}/templates/{template_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_template(token: str, name: str, client_id: int, home: bool) -> Dict[str, Any]:
    """Creates a new template in Joomla with the given name and client ID."""
    url = f"{JOOMLA_API_URL}/templates"
    headers = get_headers(token)
    data = {
        "name": name,
        "client_id": client_id,
        "home": home
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_template(token: str, template_id: int, name: str, client_id: int, home: bool) -> Dict[str, Any]:
    """Edits an existing template in Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/templates/{template_id}"
    headers = get_headers(token)
    data = {
        "name": name,
        "client_id": client_id,
        "home": home
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_template(token: str, template_id: int) -> Dict[str, Any]:
    """Deletes a template in Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/templates/{template_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return {"message": "Template deleted successfully"}
