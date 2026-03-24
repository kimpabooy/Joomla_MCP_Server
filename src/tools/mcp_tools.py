# from fastmcp import FastMCP
# from os import getenv
# from src.services.articles_service import (
#     get_joomla_articles,
#     get_joomla_article,
#     create_joomla_article,
#     publish_joomla_article,
#     unpublish_joomla_article,
#     trash_joomla_article,
#     delete_joomla_article,
#     edit_joomla_article,
#     copy_joomla_article,
#     get_unpublished_joomla_articles
# )
# from src.services.users_service import (
#     get_joomla_users,
#     get_joomla_user,
#     create_joomla_user,
#     delete_joomla_user,
#     edit_joomla_user
# )
# from src.services.menus_service import (
#     get_joomla_menus,
#     get_joomla_menu,
#     create_joomla_menu,
#     edit_joomla_menu,
#     delete_joomla_menu,
#     get_joomla_menu_items,
#     get_joomla_menu_item,
#     create_joomla_menu_item,
#     edit_joomla_menu_item,
#     delete_joomla_menu_item
# )
# from src.services.tags_service import (
#     get_joomla_tags,
#     get_joomla_tag,
#     create_joomla_tag,
#     edit_joomla_tag,
#     delete_joomla_tag,
#     get_joomla_tag_items,
#     get_joomla_tag_item,
#     create_joomla_tag_item,
#     edit_joomla_tag_item,
#     delete_joomla_tag_item
# )
# from src.services.redirects_service import (
#     get_joomla_redirects,
#     get_joomla_redirect,
#     create_joomla_redirect,
#     edit_joomla_redirect,
#     delete_joomla_redirect
# )

# """
# This module defines the MCP tools that allow the LLM to interact with Joomla articles.
# Each tool corresponds to a specific action and calls the appropriate function from the modular Joomla service files.
# The tools are decorated with @mcp.tool() to be registered with the FastMCP server.
# The module also includes a helper function to format article data into a more readable structure before returning it to the LLM.
# """

# mcp = FastMCP("Joomla MCP Server")


# def get_token() -> str:
#     token = getenv("JOOMLA_API_TOKEN")
#     if not token:
#         raise ValueError("JOOMLA_API_TOKEN saknas i miljövariabler!")
#     return token


# @mcp.tool()
# def delete_tag(tag_id: int) -> dict:
#     """Deletes a tag from Joomla based on its ID."""
#     try:
#         result = delete_joomla_tag(get_token(), tag_id)
#         return result
#     except Exception as e:
#         return {"error": str(e)}


# @mcp.tool()
# def get_tag_items(tag_id: int) -> list[dict]:
#     """Fetches all items associated with a specific tag from Joomla and returns a list of formatted tag item data."""
#     items = get_joomla_tag_items(get_token(), tag_id)
#     return [{
#         "id": item.get("id"),
#         "type": item.get("attributes", {}).get("type"),
#         "item_id": item.get("attributes", {}).get("item_id")
#     } for item in items]


# @mcp.tool()
# def get_tag_item(tag_id: int, item_id: int) -> dict:
#     """Fetches details for a specific tag item based on its ID and the tag it belongs to."""
#     item = get_joomla_tag_item(get_token(), tag_id, item_id)
#     return {
#         "id": item.get("id"),
#         "type": item.get("attributes", {}).get("type"),
#         "item_id": item.get("attributes", {}).get("item_id")
#     }


# @mcp.tool()
# def create_tag_item(tag_id: int, type: str, item_id: int) -> dict:
#     """Creates a new tag item under a specific tag in Joomla."""
#     try:
#         result = create_joomla_tag_item(get_token(), tag_id, item_id)
#         return {
#             "id": result.get("id"),
#             "type": result.get("attributes", {}).get("type"),
#             "item_id": result.get("attributes", {}).get("item_id")
#         }
#     except Exception as e:
#         return {"error": str(e)}


# @mcp.tool()
# def edit_tag_item(tag_id: int, item_id: int, type: str, new_item_id: int) -> dict:
#     """Edits an existing tag item under a specific tag in Joomla."""
#     try:
#         result = edit_joomla_tag_item(
#             get_token(), tag_id, item_id, new_item_id)
#         return {
#             "id": result.get("id"),
#             "type": result.get("attributes", {}).get("type"),
#             "item_id": result.get("attributes", {}).get("item_id")
#         }
#     except Exception as e:
#         return {"error": str(e)}


# @mcp.tool()
# def delete_tag_item(tag_id: int, item_id: int) -> dict:
#     """Deletes a tag item under a specific tag in Joomla."""
#     try:
#         result = delete_joomla_tag_item(get_token(), tag_id, item_id)
#         return result
#     except Exception as e:
#         return {"error": str(e)}

# ### --- REDIRECTS --- ###


# @mcp.tool()
# def get_redirects() -> list[dict]:
#     """Fetches all redirects from Joomla and returns a list of formatted redirect data."""
#     redirects = get_joomla_redirects(get_token())
#     return [{
#         "id": redirect.get("id"),
#         "source": redirect.get("attributes", {}).get("source"),
#         "destination": redirect.get("attributes", {}).get("destination")
#     } for redirect in redirects]


# @mcp.tool()
# def get_redirect(redirect_id: int) -> dict:
#     """Fetches details for a specific redirect based on its ID."""
#     redirect = get_joomla_redirect(get_token(), redirect_id)
#     return {
#         "id": redirect.get("id"),
#         "source": redirect.get("attributes", {}).get("source"),
#         "destination": redirect.get("attributes", {}).get("destination")
#     }


# @mcp.tool()
# def create_redirect(source: str, destination: str) -> dict:
#     """Creates a new redirect in Joomla with the given source and destination."""
#     try:
#         result = create_joomla_redirect(get_token(), source, destination)
#         return {
#             "id": result.get("id"),
#             "source": result.get("attributes", {}).get("source"),
#             "destination": result.get("attributes", {}).get("destination")
#         }
#     except Exception as e:
#         return {"error": str(e)}


# @mcp.tool()
# def edit_redirect(redirect_id: int, source: str, destination: str) -> dict:
#     """Edits an existing redirect in Joomla based on its ID with new source and destination."""
#     try:
#         result = edit_joomla_redirect(
#             get_token(), redirect_id, source, destination)
#         return {
#             "id": result.get("id"),
#             "source": result.get("attributes", {}).get("source"),
#             "destination": result.get("attributes", {}).get("destination")
#         }
#     except Exception as e:
#         return {"error": str(e)}


# @mcp.tool()
# def delete_redirect(redirect_id: int) -> dict:
#     """Deletes a redirect in Joomla based on its ID."""
#     try:
#         result = delete_joomla_redirect(get_token(), redirect_id)
#         return result
#     except Exception as e:
#         return {"error": str(e)}
