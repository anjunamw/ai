# backend/app/services/news.py
import os
from typing import Dict, List

import requests
from newsapi import NewsApiClient

from backend.app.core.config import settings
from backend.app.core.llm import generate_text


async def fetch_articles(user: str) -> str:
    news_api_key = os.getenv("NEWS_API_KEY")
    if not news_api_key:
        return "News API key not configured."
    try:
        newsapi = NewsApiClient(api_key=news_api_key)
        top_headlines = newsapi.get_top_headlines(sources="bbc-news,cnn")
        if top_headlines and top_headlines.get("articles"):
            return f"Fetched {len(top_headlines.get('articles'))} articles"
        else:
            return "No articles found"
    except Exception as e:
        print(f"Error fetching news articles: {e}")
        return "An error occurred fetching news articles"
