# backend/app/api/jira.py
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

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
    try:
        return await jira_service.fetch_issues(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/draft_comment")
async def draft_comment(issueId: str, user: str = Depends(get_current_user)):
    try:
        return {"comment": await jira_service.draft_comment(issueId, user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/add_comment")
async def add_comment(comment: str, user: str = Depends(get_current_user)):
    try:
        return {"message": await jira_service.add_comment(comment, user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
