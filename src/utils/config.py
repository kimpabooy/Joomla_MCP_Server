"""
Konfigurations- och miljövariabel-hantering för Joomla MCP.
"""

import os
from fastmcp import FastMCP
mcp = FastMCP("Joomla MCP Server")


def get_token() -> str:
    token = os.getenv("JOOMLA_API_TOKEN")
    if not token:
        raise ValueError("JOOMLA_API_TOKEN saknas i miljövariabler!")
    return token


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }
