from fastapi import APIRouter
from src.tools.articles import get_articles, get_all_endpoints
from os import getenv

router = APIRouter()


# //////////////////////////////////////////////////////////////////////////////////////
# Lägg till fler endpoints här, t.ex. för att kommunicera med Joomla API, hantera användare, etc.
# //////////////////////////////////////////////////////////////////////////////////////
@router.get("/endpoints")
def endpoints():
    return get_all_endpoints(router)


# //////////////////////////////////////////////////////////////////////////////////////
# Endpoint för att hämta artiklar från Joomla API
# //////////////////////////////////////////////////////////////////////////////////////
@router.get("/articles")
def articles():
    JOOMLA_API_TOKEN = getenv("JOOMLA_API_TOKEN")

    if not JOOMLA_API_TOKEN:
        return {"error": "JOOMLA_API_TOKEN saknas i miljövariabler!"}

    return get_articles(JOOMLA_API_TOKEN)
