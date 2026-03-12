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
    """Hämtar alla artiklar från Joomla och returnerar en lista med formaterad artikeldata."""
    url = f"{JOOMLA_URL}/content/articles"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


def get_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    """Hämtar detaljer för en specifik artikel baserat på dess ID."""
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
