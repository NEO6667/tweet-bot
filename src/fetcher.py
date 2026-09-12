import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_latest_news():
    url = "https://newsdata.io/api/1/latest"
    params = {
        "apikey": NEWS_API_KEY,
        "q": "artificial intelligence OR software engineering OR engineering",
        "category": "technology",
        "language": "en",
        "size": 10,
        "removeduplicate": "1",
    }
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    articles = []
    for item in data.get("results", []):
        articles.append({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "link": item.get("link", ""),
            "image_url": item.get("image_url", ""),
            "pub_date": item.get("pubDate", ""),
            "source": item.get("source_id", ""),
        })
    return articles