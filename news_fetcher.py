import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(topic: str, num_articles: int = 5) -> list[dict]:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": num_articles,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        return []

    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "url": article.get("url", ""),
            "publishedAt": article.get("publishedAt", ""),
            "source": article.get("source", {}).get("name", "")
        })

    return articles