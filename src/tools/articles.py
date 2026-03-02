from pydantic import BaseModel
from src.services.joomla_service import get_joomla_articles


class MCPRequest(BaseModel):
    tool: str
    arguments: dict | None = None
    JOOMLA_API_TOKEN: str


def get_articles(JOOMLA_API_TOKEN: str):
    articles = get_joomla_articles(JOOMLA_API_TOKEN)
    return MCPRequest(tool="get_articles", arguments={"articles": articles}, JOOMLA_API_TOKEN=JOOMLA_API_TOKEN).model_dump()
