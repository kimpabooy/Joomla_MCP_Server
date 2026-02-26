from fastapi import APIRouter
from src.tools.articles import get_articles, add_article

router = APIRouter()


@router.get("/articles")
def articles():
    return get_articles()


@router.post("/add_article")
def add_article_route(article: dict):
    return add_article(article)
