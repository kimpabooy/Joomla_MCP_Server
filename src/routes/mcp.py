from fastapi import APIRouter, Request
from pydantic import BaseModel
from src.tools.articles import get_article_id, get_articles, get_all_endpoints, publish_article, unpublish_article, trash_article
from os import getenv
import requests


# Request models for body-based endpoints (POST/PATCH)
class PostArticleRequest(BaseModel):
    title: str
    content: str


class PatchArticleRequest(BaseModel):
    id: int
    title: str
    content: str


# Gets token from environment variable and raises an error if it's not set, ensuring secure access to Joomla API.
# This function is used in all routes that require authentication to interact with the Joomla API.
def get_token():
    JOOMLA_API_TOKEN = getenv("JOOMLA_API_TOKEN")
    if not JOOMLA_API_TOKEN:
        raise ValueError("JOOMLA_API_TOKEN saknas i miljövariabler!")
    return JOOMLA_API_TOKEN


router = APIRouter()


# The chat UI (views.py) always sends GET requests via fetch().
# Generic proxy-endpoint that determines HTTP method based on the requested endpoint pattern and forwards the request to our own local routes.
@router.api_route("/mcp-proxy", methods=["GET", "POST", "PATCH", "DELETE"])
def mcp_proxy(request: Request, endpoint: str):
    from re import match

    # Explanation of RegEx:
    # r = raw string,
    # ^ = start of string,
    # $ = end of string,
    # \d+ = one or more digits

    # RegEx exampeles:
    # GET endpoints: (r"^/articles$", "GET")
    # POST endpoints: (r"^/articles/\d+/post_article$", "POST")
    # PATCH endpoints: (r"^/articles/\d+/unpublish$", "PATCH")
    # DELETE endpoints: (r"^/articles/\d+/delete$", "DELETE")

    # Method mapping based on endpoint patterns (regex → HTTP method)
    # Tuple
    ENDPOINT_METHOD_MAP = [
        (r"^/articles$",               "GET"),
        (r"^/articles/\d+$",           "GET"),
        (r"^/articles/\d+/trash$",     "PATCH"),
        (r"^/articles/\d+/publish$",   "PATCH"),
        (r"^/articles/\d+/unpublish$", "PATCH"),
        (r"^/articles/\d+/post_article$", "POST"),
        # Add more as needed...
    ]

    # Determine the HTTP method based on the endpoint pattern
    # if no pattern matches, default to GET
    method = "GET"
    for pattern, mapped_method in ENDPOINT_METHOD_MAP:
        if match(pattern, endpoint):
            method = mapped_method
            break

    # Build URL to our own local server and forward the request
    base_url = str(request.base_url).rstrip("/")
    url = f"{base_url}{endpoint}"
    response = requests.request(method, url)

    # Debugging output to verify the proxy method is working correctly
    print(f"[Proxy] Metod: {method}, URL: {url}")
    print(f"[Proxy] Statuskod: {response.status_code}")
    print(f"[Proxy] Respons: {response.text}")

    try:
        return response.json()
    except Exception:
        return {"error": "Kunde inte tolka svaret"}


"""
GET-endpoints
"""


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


"""
PATCH-endpoints
"""


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


"""
DELETE-endpoints
"""
