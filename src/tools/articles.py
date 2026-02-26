from pydantic import BaseModel


class MCPRequest(BaseModel):
    tool: str
    arguments: dict | None = None


articles = [
    {"title": "Article 1", "content": "This is the content of article 1."},
    {"title": "Article 2", "content": "This is the content of article 2."},
    {"title": "Article 3", "content": "This is the content of article 3."}
]


def get_articles():
    return MCPRequest(tool="get_articles", arguments={"articles": articles}).model_dump()


def add_article(article: dict):
    articles.append(article)
    return MCPRequest(tool="add_article", arguments={"message": f"Article: {article['title']} added successfully!"}).model_dump()
