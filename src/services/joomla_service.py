# import token

import requests

# get .env variabler
from os import getenv
from typing import Any, Dict, List, Optional

TOKEN = getenv("JOOMLA_API_TOKEN")
JOOMLA_URL = getenv("JOOMLA_URL")
CONTENT_TYPE = "application/json"
ACCEPT = "*/*"


# Funktion för att skapa headers med autentisering
def get_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": CONTENT_TYPE,
        "Accept": ACCEPT
    }


# Funktion för att hämta artiklar från Joomla API
def get_joomla_articles(token: str) -> List[Dict[str, Any]]:
    url = f"{JOOMLA_URL}/content/articles"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    # Kastar ett HTTPError om statuskoden indikerar ett fel (4xx eller 5xx)
    response.raise_for_status()
    return response.json().get("data", [])
