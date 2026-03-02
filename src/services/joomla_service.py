import token

import requests

# get .env variabler
from os import getenv
from typing import Any, Dict, List, Optional

TOKEN = getenv("JOOMLA_API_TOKEN")
JOOMLA_URL = getenv("JOOMLA_URL")
CONTENT_TYPE = "application/json"
ACCEPT = "*/*"


def get_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": CONTENT_TYPE,
        "Accept": ACCEPT
    }


def get_joomla_articles(token: str) -> List[Dict[str, Any]]:
    """
    Hämtar artiklar från Joomla API.
    Lägg till autentisering (t.ex. Bearer-token) om det krävs.
    """
    url = f"{JOOMLA_URL}/content/articles"
    headers = get_headers(token)
    print("[DEBUG] Joomla API URL:", url)
    print("[DEBUG] Joomla API headers:", headers)
    response = requests.get(url, headers=headers)
    print("[DEBUG] Joomla API response status:", response.status_code)
    print("[DEBUG] Joomla API response text:", response.text)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print("Joomla API error:", response.status_code, response.text)
        raise
    return response.json().get("data", [])
