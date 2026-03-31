"""
Service functions for Joomla redirects.
"""

import requests
import os
from src.utils.config import get_headers
from typing import Any, Dict, List
JOOMLA_API_URL = os.getenv("JOOMLA_API_URL")


def get_joomla_redirects(token: str) -> List[Dict[str, Any]]:
    """Fetches all redirects from Joomla and returns a list of formatted redirect data."""
    url = f"{JOOMLA_API_URL}/redirects"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_redirect(token: str, redirect_id: int) -> Dict[str, Any]:
    """Fetches details for a specific redirect based on its ID."""
    url = f"{JOOMLA_API_URL}/redirects/{redirect_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_redirect(token: str, source: str, destination: str) -> Dict[str, Any]:
    """Creates a new redirect in Joomla with the given source and destination URLs."""
    url = f"{JOOMLA_API_URL}/redirects"
    headers = get_headers(token)
    data = {
        "source": source,
        "destination": destination,
        "language": "*"
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_redirect(token: str, redirect_id: int, source: str, destination: str) -> Dict[str, Any]:
    """Edits an existing redirect in Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/redirects/{redirect_id}"
    headers = get_headers(token)
    data = {
        "source": source,
        "destination": destination,
        "language": "*"
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_redirect(token: str, redirect_id: int) -> Dict[str, Any]:
    """Deletes a redirect from Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/redirects/{redirect_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if response.status_code == 404:
        raise Exception(f"Redirect with ID {redirect_id} not found.")

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return {
        "message": f"Redirect {redirect_id} has been deleted.",
    }
