from fastmcp import FastMCP
from os import getenv
from src.services.joomla_service import (
    create_joomla_article,
    get_joomla_articles,
    get_joomla_article,
    publish_joomla_article,
    unpublish_joomla_article,
    trash_joomla_article,
    remove_joomla_article,
    edit_joomla_article,
    copy_joomla_article,
    get_joomla_users,
    get_joomla_user,
    create_joomla_user,
    delete_joomla_user,
    edit_joomla_user,
    get_unpublished_joomla_articles
)

"""
This module defines the MCP tools that allow the LLM to interact with Joomla articles.
Each tool corresponds to a specific action and calls the appropriate function from joomla_service.
The tools are decorated with @mcp.tool() to be registered with the FastMCP server.
The module also includes a helper function to format article data into a more readable structure before returning it to the LLM.
"""

mcp = FastMCP("Joomla MCP Server")


def get_token() -> str:
    token = getenv("JOOMLA_API_TOKEN")
    if not token:
        raise ValueError("JOOMLA_API_TOKEN saknas i miljövariabler!")
    return token


# Helper function to format article data into a more readable structure
def format_article_data(article: dict) -> dict:
    attributes = article.get("attributes", {})
    return {
        "id": article.get("id"),
        "title": attributes.get("title"),
        "alias": attributes.get("alias"),
        "state": attributes.get("state") == 1 and "[1] / Published"
        or (attributes.get("state") == 0 and "[0] / Unpublished"
            or (attributes.get("state") == -2 and "[-2] / Trashed"
            or "[Unknown]")),
        "created_by": attributes.get("created_by"),
        "created": attributes.get("created"),
        "last_modified": attributes.get("modified")
    }


#### --- ARTICLES --- ###

@mcp.tool()
def list_articles() -> list[dict]:
    """Fetches all articles from Joomla and returns a list of formatted article data."""
    articles = get_joomla_articles(get_token())
    return [format_article_data(article) for article in articles]


@mcp.tool()
def get_article(article_id: int) -> dict:
    """Fetches details for a specific article based on its ID."""
    article = get_joomla_article(get_token(), article_id)
    return format_article_data(article)


@mcp.tool()
def publish(article_id: int) -> dict:
    """Publishes an article based on its ID."""
    result = publish_joomla_article(get_token(), article_id)
    return format_article_data(result)


@mcp.tool()
def unpublish(article_id: int) -> dict:
    """Unpublishes an article based on its ID."""
    result = unpublish_joomla_article(get_token(), article_id)
    return format_article_data(result)


@mcp.tool()
def trash(article_id: int) -> dict:
    """Trashes an article based on its ID."""
    result = trash_joomla_article(get_token(), article_id)
    return format_article_data(result)

@mcp.tool()
def get_unpublished_articles() -> list[dict]:
    """Fetches all unpublished articles from Joomla."""
    articles = get_unpublished_joomla_articles(get_token())
    return [format_article_data(article) for article in articles]


@mcp.tool()
def create_article(title: str, content: str) -> dict:
    """Creates a new article with the given title and content."""
    try:
        result = create_joomla_article(get_token(), title, content)
        return format_article_data(result)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def remove_article(article_id: int) -> dict:
    """Permanently deletes an article based on its ID."""
    try:
        result = remove_joomla_article(get_token(), article_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_article(article_id: int, title: str, content: str) -> dict:
    """Edits an existing article based on its ID with new title and content. Alias updates automatically."""
    try:
        result = edit_joomla_article(get_token(), article_id, title, content)
        return format_article_data(result)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def copy_article(article_id: int, new_title: str) -> dict:
    """Creates a copy of an existing article based on its ID. The new article will have the provided title and the same content as the original."""
    try:
        result = copy_joomla_article(get_token(), article_id, new_title)
        return format_article_data(result)
    except Exception as e:
        return {"error": str(e)}

### --- USERS --- ###


@mcp.tool()
def get_users() -> list[dict]:
    """Fetches all users from Joomla and returns a list of formatted user data."""
    users = get_joomla_users(get_token())
    return [{
        "id": user.get("id"),
        "name": user.get("attributes", {}).get("name")}
        for user in users
    ]


@mcp.tool()
def get_user(user_id: int) -> dict:
    """Fetches details for a specific user based on their ID."""
    user = get_joomla_user(get_token(), user_id)
    return {
        "id": user.get("id"),
        "name": user.get("attributes", {}).get("name"),
        "username": user.get("attributes", {}).get("username"),
        "email": user.get("attributes", {}).get("email")
    }


@mcp.tool()
def create_user(name: str, username: str, email: str, password: str) -> dict:
    """Creates a new user in Joomla with the given details."""
    try:
        result = create_joomla_user(
            get_token(), name, username, email, password)
        return {
            "id": result.get("id"),
            "name": result.get("attributes", {}).get("name"),
            "username": result.get("attributes", {}).get("username"),
            "email": result.get("attributes", {}).get("email")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_user(user_id: int) -> dict:
    """Deletes a user from Joomla based on their ID."""
    try:
        result = delete_joomla_user(get_token(), user_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def edit_user(user_id: int, name: str, username: str, email: str) -> dict:
    """Edits an existing user in Joomla based on their ID. Only provided fields will be updated."""
    try:
        result = edit_joomla_user(get_token(), user_id, name, username, email)
        return {
            "id": result.get("id"),
            "name": result.get("attributes", {}).get("name"),
            "username": result.get("attributes", {}).get("username"),
            "email": result.get("attributes", {}).get("email")
        }
    except Exception as e:
        return {"error": str(e)}
