# backend/app/services/confluence.py
import os
from typing import List

from atlassian import Confluence
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.core.utils import get_current_time
from backend.app.db.database import get_db


async def index_confluence(user: str, db: Session = Depends(get_db)):
    confluence_url = os.getenv("CONFLUENCE_URL")
    confluence_api_token = os.getenv("CONFLUENCE_API_TOKEN")
    if not confluence_url or not confluence_api_token:
        return {"message": "Confluence credentials missing."}
    confluence_client = Confluence(url=confluence_url, token=confluence_api_token)
    space_keys = confluence_client.get_all_spaces()
    for space in space_keys:
        space_key = space["key"]
        page_ids = confluence_client.get_space_content_ids(
            space_key=space_key, content_type="page"
        )
        for page_id in page_ids:
            page_content = confluence_client.get_content_by_id(
                page_id, expand="body.storage"
            )
            if (
                page_content
                and "body" in page_content
                and "storage" in page_content["body"]
            ):
                html_content = page_content["body"]["storage"]["value"]
                text_content = BeautifulSoup(html_content, "html.parser").get_text(
                    separator=" ", strip=True
                )
                if text_content:
                    embedding_prompt = f"Generate a vector embedding for the following Confluence page text: {text_content}"
                    embedding = generate_text(embedding_prompt)
                    if embedding:
                        # db_record = DBRecord(type="confluence", text=text_content, embedding = embedding, source=page_id, user_id=1)
                        # db.add(db_record)
                        # db.commit()
                        print(f"Indexed page: {page_content['title']} (ID: {page_id})")
                    else:
                        print(
                            f"Failed to generate embeddings for Confluence page {page_id}."
                        )
    return {"message": f"Confluence indexing initiated at {get_current_time()}"}
