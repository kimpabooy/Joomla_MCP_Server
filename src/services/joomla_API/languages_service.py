"""
Service functions for Joomla languages.
"""

import requests
import os
from src.utils.config import get_headers
from typing import Any, Dict, List
JOOMLA_API_URL = os.getenv("JOOMLA_API_URL")


def get_joomla_languages(token: str) -> List[Dict[str, Any]]:
    """Fetches all languages from Joomla and returns a list of formatted language data."""
    url = f"{JOOMLA_API_URL}/languages"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_language(token: str, language_id: int) -> Dict[str, Any]:
    """Fetches details for a specific language based on its ID."""
    url = f"{JOOMLA_API_URL}/languages/{language_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_language(token: str, title: str, lang_code: str, image: str, published: bool) -> Dict[str, Any]:
    """Creates a new language in Joomla with the given title, language code, image, and published state."""
    url = f"{JOOMLA_API_URL}/languages"
    headers = get_headers(token)
    data = {
        "title": title,
        "lang_code": lang_code,
        "image": image,
        "published": published
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_language(token: str, language_id: int, title: str, lang_code: str, image: str, published: bool) -> Dict[str, Any]:
    """Edits an existing language in Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/languages/{language_id}"
    headers = get_headers(token)
    data = {
        "title": title,
        "lang_code": lang_code,
        "image": image,
        "published": published
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_language(token: str, language_id: int) -> None:
    """Deletes a language from Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/languages/{language_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
