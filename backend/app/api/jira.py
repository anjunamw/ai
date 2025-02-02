from typing import Dict, List

from fastapi import APIRouter, Depends

from backend.app.core.security import get_current_user
from backend.app.services import jira as jira_service

router = APIRouter(
    prefix="/jira",
    tags=["jira"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/issues")
async def get_jira_issues(
        user: str = Depends(get_current_user),
) -> List[Dict[str, str]]:
    return await jira_service.fetch_issues(user)


@router.post("/draft_comment")
async def draft_comment(issueId: str, user: str = Depends(get_current_user)):
    comment = await jira_service.draft_comment(issueId, user)
    return {"comment": comment}


@router.post("/add_comment")
async def add_comment(comment: str, user: str = Depends(get_current_user)):
    message = await jira_service.add_comment(comment, user)
    return {"message": message}
