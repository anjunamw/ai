# backend/app/core/scraping.py
import requests
from bs4 import BeautifulSoup


def scrape_url(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text_content = soup.get_text(separator=" ", strip=True)
        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error during web scraping: {e}")
        return None
