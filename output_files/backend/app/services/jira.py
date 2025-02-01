# backend/app/services/jira.py
import os
from typing import Dict, List

from fastapi import Depends
from jira import JIRA
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db
from backend.app.db.models import JIRAIssue


async def fetch_issues(
    user: str, db: Session = Depends(get_db)
) -> List[Dict[str, str]]:
    jira_server_url = os.getenv("JIRA_SERVER_URL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    if not jira_server_url or not jira_api_token:
        return []
    try:
        jira_options = {"server": jira_server_url}
        jira_client = JIRA(options=jira_options, token_auth=jira_api_token)
        issues = jira_client.search_issues(
            jql_str="assignee = currentUser()", maxResults=10
        )
        issue_list = []
        for issue in issues:
            issue_list.append(
                {
                    "id": issue.id,
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": issue.fields.status.name,
                }
            )
        return issue_list
    except Exception as e:
        print(f"Error during jira fetch: {e}")
        return []


async def draft_comment(issue_id: str, user: str) -> str | None:
    jira_server_url = os.getenv("JIRA_SERVER_URL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    if not jira_server_url or not jira_api_token:
        return "JIRA credentials not configured."
    try:
        jira_options = {"server": jira_server_url}
        jira_client = JIRA(options=jira_options, token_auth=jira_api_token)
        issue = jira_client.issue(issue_id)
        prompt = f"Draft a concise and professional comment for the following JIRA issue:\nSummary: {issue.fields.summary}\nDescription: {issue.fields.description}"
        return generate_text(prompt)
    except Exception as e:
        print(f"Error during jira draft comment: {e}")
        return "An error occurred while drafting a comment."


async def add_comment(comment: str, user: str) -> str:
    jira_server_url = os.getenv("JIRA_SERVER_URL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    if not jira_server_url or not jira_api_token:
        return "JIRA credentials not configured"
    try:
        jira_options = {"server": jira_server_url}
        jira_client = JIRA(options=jira_options, token_auth=jira_api_token)
        issue = jira_client.issue("LLMC-1")
        jira_client.add_comment(issue, comment)
        return "Comment added to JIRA successfully."
    except Exception as e:
        print(f"Error during jira add comment: {e}")
        return "An error occurred while adding a comment"
