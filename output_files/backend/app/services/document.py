# backend/app/services/document.py
from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.core.scraping import scrape_url


async def summarize_document(url: str, user: str) -> str:
    content = scrape_url(url)
    if content:
        prompt = f"Summarize this document: {content}"
        return generate_text(prompt) or "Could not generate summary"
    else:
        return "Could not scrape the given URL"
