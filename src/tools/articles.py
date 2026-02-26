from pydantic import BaseModel


class MCPRequest(BaseModel):
    tool: str
    arguments: dict | None = None


articles = [
    {"title": "Article 1", "content": "This is the content of article 1."},
    {"title": "Article 2", "content": "This is the content of article 2."},
    {"title": "Article 3", "content": "This is the content of article 3."}
]

# This function returns the list of articles in the form of an MCPRequest object, which can be used by the client to retrieve the articles from the server.

# Todo: interact with Joomla API to get articles from there as well.


def get_articles():
    return MCPRequest(tool="get_articles", arguments={"articles": articles}).model_dump()

# This function adds a new article to the list of articles and returns a response indicating that the article was added successfully.

# Todo: interact with Joomla API to add article there as well.


def add_article(article: dict):
    articles.append(article)
    return MCPRequest(
        tool="add_article",
        arguments={
            "message": f"Article: {article['title']} added successfully!"
        }
    ).model_dump()
