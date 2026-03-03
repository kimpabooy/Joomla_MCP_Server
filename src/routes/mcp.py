from fastapi import APIRouter, Query
from src.tools.articles import get_article_id, get_articles, get_all_endpoints, publish_article, unpublish_article, trash_article
from os import getenv
import requests


router = APIRouter()

base_url = getenv("SERVER_URL")


def get_token():
    JOOMLA_API_TOKEN = getenv("JOOMLA_API_TOKEN")
    if not JOOMLA_API_TOKEN:
        raise ValueError("JOOMLA_API_TOKEN saknas i miljövariabler!")
    return JOOMLA_API_TOKEN


# //////////////////////////////////////////////////////////////////////////////////////
# Generisk proxy-endpoint som avgör HTTP-metod baserat på endpoint-sträng
# //////////////////////////////////////////////////////////////////////////////////////
@router.api_route("/mcp-proxy", methods=["GET", "POST", "PATCH"])
def mcp_proxy(endpoint: str = Query(..., description="API-endpoint att anropa, t.ex. /articles/1/unpublish")):
    from re import match

    # Metodmappning baserat på endpoint-mönster (regex → HTTP-metod)
    ENDPOINT_METHOD_MAP = [
        (r"^/articles/\d+/unpublish$", "PATCH"),
        (r"^/articles/\d+/publish$",   "PATCH"),
        (r"^/articles/\d+/trash$",     "PATCH"),
        (r"^/articles/\d+$",           "GET"),
        (r"^/articles$",               "GET"),
        # Lägg till fler mönster här vid behov
    ]

    method = "GET"  # Standardmetod
    for pattern, mapped_method in ENDPOINT_METHOD_MAP:
        if match(pattern, endpoint):
            method = mapped_method
            break

    url = f"{base_url}{endpoint}"
    resp = requests.request(method, url)

    print(f"[Proxy] Metod: {method}, URL: {url}")
    print(f"[Proxy] Statuskod: {resp.status_code}")
    print(f"[Proxy] Respons: {resp.text}")

    try:
        return resp.json()
    except Exception:
        return {"error": "Kunde inte tolka svaret"}


# @router.api_route("/mcp-proxy", methods=["GET", "POST", "PATCH"])
# def mcp_proxy(endpoint: str = Query(..., description="API-endpoint att anropa, t.ex. /articles/1/unpublish")):
#     # Enkel logik för metodval, kan byggas ut med regex eller dict
#     endpoint_lower = endpoint.lower()
#     if "patch" in endpoint_lower:
#         method = "PATCH"
#     elif "post" in endpoint_lower:
#         method = "POST"
#     else:
#         method = "GET"

#     url = f"{base_url}{endpoint}"
#     resp = requests.request(method, url)

#     print(f"[Proxy] Metod: {method}, URL: {url}")
#     print(f"[Proxy] Statuskod: {resp.status_code}")
#     print(f"[Proxy] Respons: {resp.text}")

#     try:
#         return resp.json()
#     except Exception:
#         return {"error": "Kunde inte tolka svaret"}


# //////////////////////////////////////////////////////////////////////////////////////
# Lägg till fler endpoints här, t.ex. för att kommunicera med Joomla API, hantera användare, etc.
# //////////////////////////////////////////////////////////////////////////////////////
@router.get("/endpoints")
def endpoints():
    return get_all_endpoints(router)


@router.get("/help")
def help():
    return get_all_endpoints(router)


# //////////////////////////////////////////////////////////////////////////////////////
# Endpoint för att hämta artiklar från Joomla API
# //////////////////////////////////////////////////////////////////////////////////////
@router.get("/articles")
def articles():
    return get_articles(get_token())


# //////////////////////////////////////////////////////////////////////////////////////
# Endpoint för att hämta detaljerna för en specifik artikel baserat på dess ID
# //////////////////////////////////////////////////////////////////////////////////////
@router.get("/articles/{article_id}")
def article(article_id: int):
    return get_article_id(get_token(), article_id)


# //////////////////////////////////////////////////////////////////////////////////////
# Endpoint för att avpublicera en artikel baserat på dess ID
# //////////////////////////////////////////////////////////////////////////////////////
@router.patch("/articles/{article_id}/unpublish")
def unpublish(article_id: int):
    return unpublish_article(get_token(), article_id)


@router.patch("/articles/{article_id}/publish")
def publish(article_id: int):
    return publish_article(get_token(), article_id)


@router.patch("/articles/{article_id}/trash")
def trash(article_id: int):
    return trash_article(get_token(), article_id)
