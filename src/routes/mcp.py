from fastapi import APIRouter, Query
from src.tools.articles import get_article_id, get_articles, get_all_endpoints, publish_article, unpublish_article, trash_article
from os import getenv
import requests


router = APIRouter()


# Gets server URL from environment variable
def get_server_url():
    SERVER_URL = getenv("SERVER_URL")
    if not SERVER_URL:
        raise ValueError("SERVER_URL saknas i miljövariabler!")
    return SERVER_URL


# Gets token from environment variable
def get_token():
    JOOMLA_API_TOKEN = getenv("JOOMLA_API_TOKEN")
    if not JOOMLA_API_TOKEN:
        raise ValueError("JOOMLA_API_TOKEN saknas i miljövariabler!")
    return JOOMLA_API_TOKEN


# Generic proxy-endpoint that determines HTTP method based on endpoint string
@router.api_route("/mcp-proxy", methods=["GET", "POST", "PATCH"])
def mcp_proxy(endpoint: str = Query(..., description="API-endpoint att anropa, t.ex. /articles/1/unpublish")):
    from re import match

    # RegEx exampeles:
    # GET endpoints: (r"^/articles$", "GET")
    # POST endpoints: (r"^/articles/\d+/post_article$", "POST")
    # PATCH endpoints: (r"^/articles/\d+/unpublish$", "PATCH")
    # DELETE endpoints: (r"^/articles/\d+/delete$", "DELETE")

    # Method mapping based on endpoint patterns (regex → HTTP method)
    ENDPOINT_METHOD_MAP = [
        (r"^/articles/\d+/post_article$", "POST"),
        (r"^/articles/\d+/unpublish$", "PATCH"),
        (r"^/articles/\d+/publish$",   "PATCH"),
        (r"^/articles/\d+/trash$",     "PATCH"),
        (r"^/articles/\d+$",           "GET"),
        (r"^/articles$",               "GET"),
        # Add more as needed...
    ]

    method = "GET"  # Standardmetod
    for pattern, mapped_method in ENDPOINT_METHOD_MAP:
        if match(pattern, endpoint):
            method = mapped_method
            break

    url = f"{get_server_url()}{endpoint}"
    resp = requests.request(method, url)

    print(f"[Proxy] Metod: {method}, URL: {url}")
    print(f"[Proxy] Statuskod: {resp.status_code}")
    print(f"[Proxy] Respons: {resp.text}")

    try:
        return resp.json()
    except Exception:
        return {"error": "Kunde inte tolka svaret"}


# Route to show available endpoints
@router.get("/help")
def endpoints():
    return get_all_endpoints(router)


# Route to get all articles
@router.get("/articles")
def articles():
    return get_articles(get_token())


# Route to get a specific article based on its ID
@router.get("/articles/{article_id}")
def article(article_id: int):
    return get_article_id(get_token(), article_id)


# Route to unpublish an article based on its ID
@router.patch("/articles/{article_id}/unpublish")
def unpublish(article_id: int):
    return unpublish_article(get_token(), article_id)


# Route to publish an article based on its ID
@router.patch("/articles/{article_id}/publish")
def publish(article_id: int):
    return publish_article(get_token(), article_id)


# Route to trash an article based on its ID
@router.patch("/articles/{article_id}/trash")
def trash(article_id: int):
    return trash_article(get_token(), article_id)
