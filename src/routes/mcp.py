from fastapi import APIRouter
from src.tools.articles import get_articles
from os import getenv

router = APIRouter()


@router.get("/articles")
def articles():
    JOOMLA_API_TOKEN = getenv("JOOMLA_API_TOKEN")
    if not JOOMLA_API_TOKEN:
        return {"error": "JOOMLA_API_TOKEN saknas i miljövariabler!"}
    return get_articles(str(JOOMLA_API_TOKEN))

