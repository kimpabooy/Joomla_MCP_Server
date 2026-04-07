"""
Service functions for Joomla categories.
"""


import requests
from src.utils.config import get_headers, get_joomla_api_url
from typing import Any, Dict, List

JOOMLA_API_URL = get_joomla_api_url()


def get_joomla_categories(token: str) -> List[Dict[str, Any]]:
    """Fetches all categories from Joomla and returns a list of formatted category data."""
    url = f"{JOOMLA_API_URL}/banners/categories"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_category(token: str, category_id: int) -> Dict[str, Any]:
    """Fetches details for a specific category based on its ID."""
    url = f"{JOOMLA_API_URL}/banners/categories/{category_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_category(token: str, title: str, parent_id: int, published: bool) -> Dict[str, Any]:
    """Creates a new category in Joomla with the given title, parent ID, and published state."""
    url = f"{JOOMLA_API_URL}/banners/categories"
    headers = get_headers(token)
    data = {
        "title": title,
        "parent_id": parent_id,
        "published": published
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_category(token: str, category_id: int, title: str, parent_id: int, published: bool) -> Dict[str, Any]:
    """Edits an existing category in Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/banners/categories/{category_id}"
    headers = get_headers(token)
    data = {
        "title": title,
        "parent_id": parent_id,
        "published": published
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_category(token: str, category_id: int) -> None:
    """Deletes a category from Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/banners/categories/{category_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
