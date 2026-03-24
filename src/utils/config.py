"""
Konfigurations- och miljövariabel-hantering för Joomla MCP.
"""

import os
from fastmcp import FastMCP
mcp = FastMCP("Joomla MCP Server")

JOOMLA_URL = os.getenv("JOOMLA_URL")
CONTENT_TYPE = "application/json"
ACCEPT = "*/*"

def get_token() -> str:
    token = os.getenv("JOOMLA_API_TOKEN")
    if not token:
        raise ValueError("JOOMLA_API_TOKEN saknas i miljövariabler!")
    return token


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": CONTENT_TYPE,
        "Accept": ACCEPT
    }
