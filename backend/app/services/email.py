# backend/app/services/email.py
import base64
import email
import os
from email.mime.text import MIMEText
from typing import Dict, List

from fastapi import Depends
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db
from backend.app.db.models import Email


async def fetch_emails(
    user: str, db: Session = Depends(get_db)
) -> List[Dict[str, str]]:
    creds = None
    service_account_info = os.getenv("GOOGLE_SERVICE_ACCOUNT")
    if service_account_info:
        try:
            creds = service_account.Credentials.from_service_account_info(
                eval(service_account_info),
                scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            )
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
        except Exception as e:
            print(
                f"An error occurred while creating credentials from service account: {e}"
            )
    if not creds:
        return []

    try:
        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users()
            .messages()
            .list(userId="me", q="is:inbox", maxResults=10)
            .execute()
        )
        messages = results.get("messages", [])
        email_list = []
        for message in messages:
            msg = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=message["id"],
                    format="metadata",
                    metadataHeaders=["Subject", "From", "Date"],
                )
                .execute()
            )
            subject = next(
                (
                    header["value"]
                    for header in msg["payload"]["headers"]
                    if header["name"] == "Subject"
                ),
                "No Subject",
            )
            email_from = next(
                (
                    header["value"]
                    for header in msg["payload"]["headers"]
                    if header["name"] == "From"
                ),
                "Unknown Sender",
            )
            email_list.append(
                {
                    "id": message["id"],
                    "subject": subject,
                    "from": email_from,
                    "body": "",
                }
            )
        return email_list
    except Exception as e:
        print(f"An error occurred while fetching emails: {e}")
        return []


async def draft_reply(email_id: str, user: str) -> str | None:
    creds = None
    service_account_info = os.getenv("GOOGLE_SERVICE_ACCOUNT")
    if service_account_info:
        try:
            creds = service_account.Credentials.from_service_account_info(
                eval(service_account_info),
                scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            )
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
        except Exception as e:
            print(
                f"An error occurred while creating credentials from service account: {e}"
            )
    if not creds:
        return "Service account error"
    try:
        service = build("gmail", "v1", credentials=creds)
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=email_id, format="full")
            .execute()
        )
        text_parts = []
        if msg.get("payload") and msg["payload"].get("parts"):
            for part in msg["payload"]["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part["body"].get("data")
                    if data:
                        text_parts.append(base64.urlsafe_b64decode(data).decode())
        elif (
            msg.get("payload")
            and msg["payload"].get("body")
            and msg["payload"]["body"].get("data")
        ):
            data = msg["payload"]["body"].get("data")
            if data:
                text_parts.append(base64.urlsafe_b64decode(data).decode())
        email_content = "\n".join(text_parts)

        prompt = f"Draft a concise reply to the following email: {email_content}"
        return generate_text(prompt)
    except Exception as e:
        print(f"An error occurred while drafting reply: {e}")
        return "An error occurred while drafting reply"


async def send_reply(reply: str, user: str) -> str:
    creds = None
    service_account_info = os.getenv("GOOGLE_SERVICE_ACCOUNT")
    if service_account_info:
        try:
            creds = service_account.Credentials.from_service_account_info(
                eval(service_account_info),
                scopes=["https://www.googleapis.com/auth/gmail.send"],
            )
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
        except Exception as e:
            print(
                f"An error occurred while creating credentials from service account: {e}"
            )
    if not creds:
        return "Service account error"

    try:
        service = build("gmail", "v1", credentials=creds)
        message = MIMEText(reply)
        message["to"] = "test@example.com"  # Replace with actual to email
        message["from"] = "me"
        message["subject"] = "Re: Test Email"
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw_message})
            .execute()
        )
        return f"Reply sent successfully: {send_message.get('id')}"
    except Exception as e:
        print(f"An error occurred while sending reply: {e}")
        return "An error occurred while sending reply"
