import requests
from os import getenv
from typing import Any, Dict, List

"""
This module defines functions to interact with the Joomla API for managing articles.
Each function takes an authentication token and the necessary parameters to perform the action and returns the result in a structured format.
"""

JOOMLA_URL = getenv("JOOMLA_URL")
CONTENT_TYPE = "application/json"
ACCEPT = "*/*"


def _get_headers(token: str) -> Dict[str, str]:
    """Helper function to construct the headers for Joomla API requests."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": CONTENT_TYPE,
        "Accept": ACCEPT
    }


### --- CONTENT/ARTICLES --- ###

def get_joomla_articles(token: str) -> List[Dict[str, Any]]:
    """Fetches all articles from Joomla and returns a list of formatted article data."""
    url = f"{JOOMLA_URL}/content/articles"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Fetches details for a specific article based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def unpublish_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Unpublishes an article based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = _get_headers(token)
    data = {
        "state": 0  # 0 = Unpublished
    }
    response = requests.patch(url, headers=headers, json=data)

    response.raise_for_status()
    return response.json().get("data", {})


def publish_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Publishes an article based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = _get_headers(token)
    data = {
        "state": 1  # 1 = Published
    }
    response = requests.patch(url, headers=headers, json=data)

    response.raise_for_status()
    return response.json().get("data", {})


def trash_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Moves an article to the trash based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = _get_headers(token)
    data = {
        "state": -2  # -2 = Trashed
    }
    response = requests.patch(url, headers=headers, json=data)

    response.raise_for_status()
    return response.json().get("data", {})


def delete_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Permanently deletes an article based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = _get_headers(token)
    response = requests.delete(url, headers=headers)

    # if we cant find the article
    if response.status_code == 404:
        raise Exception(f"Article with ID {article_id} not found.")

    if response.status_code == 409:
        # Joomla often requires item to be trashed before permanent deletion.
        trash_joomla_article(token, article_id)
        response = requests.delete(url, headers=headers)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}"
        )

    return {
        "message": f"Article {article_id} has been permanently deleted.",
    }


def get_unpublished_joomla_articles(token: str) -> List[Dict[str, Any]]:
    """Fetches all unpublished articles from Joomla."""
    url = f"{JOOMLA_URL}/content/articles?filter[state]=0"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def create_joomla_article(token: str, title: str, articletext: str, catid: int = 2) -> Dict[str, Any]:
    """Creates a new article in Joomla with the given title and content."""
    url = f"{JOOMLA_URL}/content/articles"
    headers = _get_headers(token)
    data = {
        "title": title,
        "articletext": articletext,
        "catid": catid,
        "language": "*",
        "state": 0  # Start as unpublished
    }
    response = requests.post(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def edit_joomla_article(token: str, article_id: int, title: str, articletext: str) -> Dict[str, Any]:
    """Edits an existing article in Joomla based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = _get_headers(token)
    alias = title.lower().strip() + "- article"
    data = {
        "title": title,
        "articletext": articletext,
        "alias": alias
    }
    response = requests.patch(url, headers=headers, json=data)

    if not response.ok:
        error_detail = response.text
        raise Exception(
            f"Joomla API error ({response.status_code}): {error_detail}")
    return response.json().get("data", {})


def copy_joomla_article(token: str, article_id: int, new_title: str) -> Dict[str, Any]:
    """Copies an existing article to create a new one with a new title."""
    original_article = get_joomla_article(token, article_id)
    if not original_article:
        raise Exception(f"Article with ID {article_id} not found.")

    original_content = original_article.get(
        "attributes", {}).get("articletext", "")
    return create_joomla_article(token, new_title, original_content)


### --- USERS --- ###

def get_joomla_users(token: str) -> List[Dict[str, Any]]:
    """Fetches all users from Joomla and returns a list of formatted user data."""
    url = f"{JOOMLA_URL}/users"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_user(token: str, user_id: int) -> Dict[str, Any]:
    """Fetches details for a specific user based on their ID."""
    url = f"{JOOMLA_URL}/users/{user_id}"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_user(token: str, name: str, username: str, email: str, password: str) -> Dict[str, Any]:
    """Creates a new user in Joomla with the given details."""
    url = f"{JOOMLA_URL}/users"
    headers = _get_headers(token)
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
    url = f"{JOOMLA_URL}/users/{user_id}"
    headers = _get_headers(token)
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
    url = f"{JOOMLA_URL}/users/{user_id}"
    headers = _get_headers(token)
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

### --- MENUS --- ###


def get_joomla_menus(token: str) -> List[Dict[str, Any]]:
    """Fetches all menus from Joomla and returns a list of formatted menu data."""
    url = f"{JOOMLA_URL}/menus"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_menu(token: str, menu_id: int) -> Dict[str, Any]:
    """Fetches details for a specific menu based on its ID."""
    url = f"{JOOMLA_URL}/menus/{menu_id}"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_menu(token: str, title: str, alias: str) -> Dict[str, Any]:
    """Creates a new menu in Joomla with the given title and alias."""
    url = f"{JOOMLA_URL}/menus"
    headers = _get_headers(token)
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
    headers = _get_headers(token)
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
    headers = _get_headers(token)
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
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_menu_item(token: str, menu_id: int, item_id: int) -> Dict[str, Any]:
    """Fetches details for a specific menu item based on its ID and the menu it belongs to."""
    url = f"{JOOMLA_URL}/menus/{menu_id}/items/{item_id}"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_menu_item(token: str, menu_id: int, title: str, alias: str, link: str) -> Dict[str, Any]:
    """Creates a new menu item under a specific menu in Joomla."""
    url = f"{JOOMLA_URL}/menus/{menu_id}/items"
    headers = _get_headers(token)
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
    headers = _get_headers(token)
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
    headers = _get_headers(token)
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


### --- TAGS --- ###

def get_joomla_tags(token: str) -> List[Dict[str, Any]]:
    """Fetches all tags from Joomla and returns a list of formatted tag data."""
    url = f"{JOOMLA_URL}/content/tags"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_tag(token: str, tag_id: int) -> Dict[str, Any]:
    """Fetches details for a specific tag based on its ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_tag(token: str, title: str, alias: str) -> Dict[str, Any]:
    """Creates a new tag in Joomla with the given title and alias."""
    url = f"{JOOMLA_URL}/content/tags"
    headers = _get_headers(token)
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
    headers = _get_headers(token)
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
    headers = _get_headers(token)
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
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_tag_item(token: str, tag_id: int, item_id: int) -> Dict[str, Any]:
    """Fetches details for a specific item associated with a tag based on the tag ID and item ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}/items/{item_id}"
    headers = _get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def create_joomla_tag_item(token: str, tag_id: int, item_id: int) -> Dict[str, Any]:
    """Associates an item with a specific tag based on the tag ID and item ID."""
    url = f"{JOOMLA_URL}/content/tags/{tag_id}/items"
    headers = _get_headers(token)
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
    headers = _get_headers(token)
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
    headers = _get_headers(token)
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


# Future functions that could be added:
### --- REDIRECTS --- ###


# inte prio
### --- MESSAGES --- ###
### --- MODULES --- ###
### --- NEWSFEEDS --- ###
### --- PRIVACYS --- ###
### --- TEMPLATES --- ###
### --- LANGUAGES --- ###
