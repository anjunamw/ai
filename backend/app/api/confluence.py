# backend/app/api/confluence.py
"""
confluence.py

Provides endpoints to index and interact with Confluence content using the atlassian-python-api.
"""

from fastapi import APIRouter, Depends, HTTPException, status
import logging
from atlassian import Confluence
from datetime import datetime
from backend.app.core.config import settings
from backend.app.core.utils import get_current_time
from sqlalchemy.orm import Session
from backend.app.db.database import get_db

router = APIRouter(
    prefix="/confluence",
    tags=["confluence"],
)

@router.get("/index")
async def index_confluence(user: str, db: Session = Depends(get_db)):
    """
    Attempts to index a Confluence space by checking connectivity and credentials.
    (Full indexing and crawling should be implemented as needed.)
    """
    confluence_url = settings.get("CONFLUENCE_URL", "https://yourcompany.atlassian.net/wiki")
    confluence_api_token = settings.get("CONFLUENCE_API_TOKEN", None)
    if not confluence_url or not confluence_api_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Confluence credentials missing. Indexing not possible."
        )
    try:
        confluence_client = Confluence(url=confluence_url, token=confluence_api_token)
        # Example: Get spaces
        spaces = confluence_client.get_all_spaces(limit=10)
        return {
            "message": f"Confluence indexing initiated at {get_current_time()}.",
            "spaces_found": spaces
        }
    except Exception as e:
        logging.error(f"Error indexing Confluence: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Confluence indexing failed at {get_current_time()}. Error: {e}"
        )