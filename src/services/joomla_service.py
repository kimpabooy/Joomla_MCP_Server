import requests
from os import getenv
from typing import Any, Dict, List


TOKEN = getenv("JOOMLA_API_TOKEN")
JOOMLA_URL = getenv("JOOMLA_URL")
CONTENT_TYPE = "application/json"
ACCEPT = "*/*"


def get_headers(token: str) -> Dict[str, str]:
    """Helper function to construct the headers for Joomla API requests."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": CONTENT_TYPE,
        "Accept": ACCEPT
    }


def get_joomla_articles(token: str) -> List[Dict[str, Any]]:
    """Fetches all articles from Joomla and returns a list of formatted article data."""
    url = f"{JOOMLA_URL}/content/articles"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Fetches details for a specific article based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


def unpublish_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Unpublishes an article based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = get_headers(token)
    data = {
        "state": 0  # 0 = Unpublished
    }
    response = requests.patch(url, headers=headers, json=data)

    response.raise_for_status()
    return response.json().get("data", {})


def publish_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Publishes an article based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = get_headers(token)
    data = {
        "state": 1  # 1 = Published
    }
    response = requests.patch(url, headers=headers, json=data)

    response.raise_for_status()
    return response.json().get("data", {})


def trash_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Moves an article to the trash based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = get_headers(token)
    data = {
        "state": -2  # -2 = Trashed
    }
    response = requests.patch(url, headers=headers, json=data)

    response.raise_for_status()
    return response.json().get("data", {})


def remove_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Permanently deletes an article based on its ID."""
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = get_headers(token)
    response = requests.delete(url, headers=headers)

    response.raise_for_status()
    return {"message": f"Article {article_id} has been permanently deleted."}


def create_joomla_article(token: str, title: str, articletext: str, catid: int = 2) -> Dict[str, Any]:
    """Creates a new article in Joomla with the given title and content."""
    url = f"{JOOMLA_URL}/content/articles"
    headers = get_headers(token)
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
    headers = get_headers(token)
    # generated_alias = alias if alias else title.lower().replace(" ", "-")
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
