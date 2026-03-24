"""
Service functions for Joomla menus.
"""

from src.utils.config import JOOMLA_URL, get_headers
from typing import Any, Dict, List
import requests


def get_joomla_menus(token: str) -> List[Dict[str, Any]]:
    """Fetches all menus from Joomla and returns a list of formatted menu data."""
    url = f"{JOOMLA_URL}/menus"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_menu(token: str, menu_id: int) -> Dict[str, Any]:
    """Fetches details for a specific menu based on its ID."""
    url = f"{JOOMLA_URL}/menus/{menu_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_menu(token: str, title: str, alias: str) -> Dict[str, Any]:
    """Creates a new menu in Joomla with the given title and alias."""
    url = f"{JOOMLA_URL}/menus"
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


def edit_joomla_menu(token: str, menu_id: int, title: str, alias: str) -> Dict[str, Any]:
    """Edits an existing menu in Joomla based on its ID."""
    url = f"{JOOMLA_URL}/menus/{menu_id}"
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


def delete_joomla_menu(token: str, menu_id: int) -> Dict[str, Any]:
    """Deletes a menu from Joomla based on its ID."""
    url = f"{JOOMLA_URL}/menus/{menu_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if response.status_code == 404:
        raise Exception(f"Menu with ID {menu_id} not found.")

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return {
        "message": f"Menu {menu_id} has been deleted.",
    }


def get_joomla_menu_items(token: str, menu_id: int) -> List[Dict[str, Any]]:
    """Fetches all menu items for a specific menu based on its ID."""
    url = f"{JOOMLA_URL}/menus/{menu_id}/items"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_menu_item(token: str, menu_id: int, item_id: int) -> Dict[str, Any]:
    """Fetches details for a specific menu item based on its ID and the menu it belongs to."""
    url = f"{JOOMLA_URL}/menus/{menu_id}/items/{item_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_menu_item(token: str, menu_id: int, title: str, alias: str, link: str) -> Dict[str, Any]:
    """Creates a new menu item under a specific menu in Joomla."""
    url = f"{JOOMLA_URL}/menus/{menu_id}/items"
    headers = get_headers(token)
    data = {
        "title": title,
        "alias": alias,
        "link": link,
        "language": "*"
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_menu_item(token: str, menu_id: int, item_id: int, title: str, alias: str, link: str) -> Dict[str, Any]:
    """Edits an existing menu item under a specific menu in Joomla based on its ID."""
    url = f"{JOOMLA_URL}/menus/{menu_id}/items/{item_id}"
    headers = get_headers(token)
    data = {
        "title": title,
        "alias": alias,
        "link": link
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def delete_joomla_menu_item(token: str, menu_id: int, item_id: int) -> Dict[str, Any]:
    """Deletes a menu item from a specific menu in Joomla based on its ID."""
    url = f"{JOOMLA_URL}/menus/{menu_id}/items/{item_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    if response.status_code == 404:
        raise Exception(
            f"Menu item with ID {item_id} not found in menu {menu_id}.")

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return {
        "message": f"Menu item {item_id} has been deleted from menu {menu_id}.",
    }
