from pydantic import BaseModel
from src.services.joomla_service import get_joomla_articles


class MCPRequest(BaseModel):  # JSON-serialiserbar modell för att representera ett verktygsanrop
    tool: str
    arguments: dict | None = None


# //////////////////////////////////////////////////////////////////////////////////////

# Funktion för att hämta alla artiklar från Joomla API
def get_articles(JOOMLA_API_TOKEN: str):
    articles = get_joomla_articles(JOOMLA_API_TOKEN)
    return MCPRequest(tool="get_articles", arguments={"articles": articles}).model_dump()
