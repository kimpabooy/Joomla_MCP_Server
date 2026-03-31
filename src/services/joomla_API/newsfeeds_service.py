"""
Service functions for Joomla newsfeeds.
"""

import requests
import os
from src.utils.config import get_headers
from typing import Any, Dict, List
JOOMLA_API_URL = os.getenv("JOOMLA_API_URL")


def get_joomla_newsfeeds(token: str) -> List[Dict[str, Any]]:
    """Fetches all newsfeeds from Joomla and returns a list of formatted newsfeed data."""
    url = f"{JOOMLA_API_URL}/newsfeeds"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_newsfeed(token: str, newsfeed_id: int) -> Dict[str, Any]:
    """Fetches details for a specific newsfeed based on its ID."""
    url = f"{JOOMLA_API_URL}/newsfeeds/{newsfeed_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_newsfeed(token: str, title: str, link: str, published: bool) -> Dict[str, Any]:
    """Creates a new newsfeed in Joomla with the given title, link, and published state."""
    url = f"{JOOMLA_API_URL}/newsfeeds"
    headers = get_headers(token)
    data = {
        "title": title,
        "link": link,
        "published": published
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_newsfeed(token: str, newsfeed_id: int, title: str, link: str, published: bool) -> Dict[str, Any]:
    """Edits an existing newsfeed in Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/newsfeeds/{newsfeed_id}"
    headers = get_headers(token)
    data = {
        "title": title,
        "link": link,
        "published": published
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_newsfeed(token: str, newsfeed_id: int) -> Dict[str, Any]:
    """Deletes an existing newsfeed in Joomla based on its ID."""
    url = f"{JOOMLA_API_URL}/newsfeeds/{newsfeed_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return {"message": "Newsfeed deleted successfully."}
