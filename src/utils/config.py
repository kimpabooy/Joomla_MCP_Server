"""
Konfigurations- och miljövariabel-hantering för Joomla MCP.
"""

import os
from urllib.parse import urlsplit, urlunsplit
from fastmcp import FastMCP
mcp = FastMCP("Joomla MCP Server")


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY saknas i miljövariabler!")
    return api_key


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


def get_joomla_api_url() -> str:
    """Returns a container-safe Joomla API base URL from JOOMLA_API_URL."""
    raw_url = os.getenv("JOOMLA_API_URL", "").strip()
    if not raw_url:
        raise ValueError("JOOMLA_API_URL saknas i miljövariabler!")

    # Detect if running inside Docker by checking /.dockerenv
    in_docker = os.path.isfile("/.dockerenv")

    # Only normalize localhost to host.docker.internal if running inside Docker.
    # Locally, localhost is already correct.
    if not in_docker:
        return raw_url

    parsed = urlsplit(raw_url)
    hostname = parsed.hostname

    # If hostname is localhost-like, replace with host.docker.internal for Docker access.
    if hostname in {"localhost", "127.0.0.1", "host.docker.internal.localhost"}:
        netloc = parsed.netloc.replace(hostname, "host.docker.internal", 1)
        return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))

    return raw_url
