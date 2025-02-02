# backend/app/api/document.py
"""
document.py

Provides an endpoint to summarize a document from a given URL by scraping its content and using the LLM.
"""

from fastapi import APIRouter, HTTPException, status

from backend.app.core.llm import generate_text
from backend.app.core.scraping import scrape_url

router = APIRouter(
    prefix="/document",
    tags=["document"],
)


@router.post("/summarize")
async def summarize_document(url: str, user: str):
    content = scrape_url(url)
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Could not scrape content from the provided URL.")
    prompt = f"Summarize the following document in a concise and clear manner:\n\n{content}\n\nSummary:"
    summary = generate_text(prompt)
    if not summary:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="LLM failed to generate a summary.")
    return {"summary": summary}
