"""
Service functions for Joomla tags.
"""

from src.utils.config import JOOMLA_URL, get_headers
from typing import Any, Dict, List
import requests


def get_joomla_tags(token: str) -> List[Dict[str, Any]]:
    """Fetches all tags from Joomla and returns a list of formatted tag data."""
    url = f"{JOOMLA_URL}/content/tags"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_tag(token: str, tag_id: int) -> Dict[str, Any]:
    """Fetches details for a specific tag based on its ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_tag(token: str, title: str, alias: str) -> Dict[str, Any]:
    """Creates a new tag in Joomla with the given title and alias."""
    url = f"{JOOMLA_URL}/content/tags"
    headers = get_headers(token)
    data = {
        "title": title,
        "alias": alias,
        "language": "*"
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_tag(token: str, tag_id: int, title: str, alias: str) -> Dict[str, Any]:
    """Edits an existing tag in Joomla based on its ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}"
    headers = get_headers(token)
    data = {
        "title": title,
        "alias": alias
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_tag(token: str, tag_id: int) -> Dict[str, Any]:
    """Deletes a tag from Joomla based on its ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if response.status_code == 404:
        raise Exception(f"Tag with ID {tag_id} not found.")

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return {
        "message": f"Tag {tag_id} has been deleted.",
    }


def get_joomla_tag_items(token: str, tag_id: int) -> List[Dict[str, Any]]:
    """Fetches all items associated with a specific tag based on its ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}/items"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_tag_item(token: str, tag_id: int, item_id: int) -> Dict[str, Any]:
    """Fetches details for a specific item associated with a tag based on the tag ID and item ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}/items/{item_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_tag_item(token: str, tag_id: int, item_id: int) -> Dict[str, Any]:
    """Associates an item with a specific tag based on the tag ID and item ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}/items"
    headers = get_headers(token)
    data = {
        "item_id": item_id
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_tag_item(token: str, tag_id: int, item_id: int, new_item_id: int) -> Dict[str, Any]:
    """Updates the association of an item with a specific tag based on the tag ID and item ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}/items/{item_id}"
    headers = get_headers(token)
    data = {
        "item_id": new_item_id
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_tag_item(token: str, tag_id: int, item_id: int) -> Dict[str, Any]:
    """Removes the association of an item with a specific tag based on the tag ID and item ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}/items/{item_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if response.status_code == 404:
        raise Exception(
            f"Association of item {item_id} with tag {tag_id} not found.")

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return {
        "message": f"Association of item {item_id} with tag {tag_id} has been removed.",
    }
