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


### --- ARTICLES --- ###

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


def remove_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
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

# Future functions that could be added:
### --- BANNERS --- ###
### --- CONTACTS --- ###
### --- CONTENTS --- ###
### --- LANGUAGES --- ###
### --- MENUS --- ###
### --- MESSAGES --- ###
### --- MODULES --- ###
### --- NEWSFEEDS --- ###
### --- PRIVACYS --- ###
### --- REDIRECTS --- ###
### --- TAGS --- ###
### --- TEMPLATES --- ###
