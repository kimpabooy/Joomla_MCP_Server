import requests
from os import getenv
from typing import Any, Dict, List

TOKEN = getenv("JOOMLA_API_TOKEN")
JOOMLA_URL = getenv("JOOMLA_URL")
CONTENT_TYPE = "application/json"
ACCEPT = "*/*"


# //////////////////////////////////////////////////////////////////////////////////////
#  Hjälpfunktion för att skapa headers med autentisering
# //////////////////////////////////////////////////////////////////////////////////////
def get_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": CONTENT_TYPE,
        "Accept": ACCEPT
    }


# //////////////////////////////////////////////////////////////////////////////////////
# Funktion för att hämta alla artiklar från Joomla API
# //////////////////////////////////////////////////////////////////////////////////////
def get_joomla_articles(token: str) -> List[Dict[str, Any]]:
    url = f"{JOOMLA_URL}/content/articles"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", [])


# //////////////////////////////////////////////////////////////////////////////////////
# Funktion för att hämta detaljerna för en specifik artikel baserat på dess ID
# //////////////////////////////////////////////////////////////////////////////////////
def get_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json().get("data", {})


# //////////////////////////////////////////////////////////////////////////////////////
# Funktion för att avpublisera en artikel baserat på dess ID
# //////////////////////////////////////////////////////////////////////////////////////
def unpublish_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = get_headers(token)
    data = {
        "state": 0  # 0 = Unpublished
    }
    response = requests.patch(url, headers=headers, json=data)

    response.raise_for_status()
    return response.json().get("data", {})


# //////////////////////////////////////////////////////////////////////////////////////
# Funktion för att publicera en artikel baserat på dess ID
# //////////////////////////////////////////////////////////////////////////////////////
def publish_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = get_headers(token)
    data = {
        "state": 1  # 1 = Published
    }
    response = requests.patch(url, headers=headers, json=data)

    response.raise_for_status()
    return response.json().get("data", {})


def trash_joomla_article(token: str, article_id: int) -> Dict[str, Any]:
    url = f"{JOOMLA_URL}/content/articles/{article_id}"
    headers = get_headers(token)
    data = {
        "state": -2  # -2 = Trashed
    }
    response = requests.patch(url, headers=headers, json=data)

    response.raise_for_status()
    return response.json().get("data", {})
