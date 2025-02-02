# backend/app/services/email.py
import base64
import os
import logging
from email.mime.text import MIMEText
from typing import Dict, List

from fastapi import HTTPException, status
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def get_gmail_service():
    """
    Returns an authorized Gmail API service instance.
    Expects a credentials file specified by GMAIL_CREDENTIALS_FILE in configuration.
    """
    creds = None
    credentials_file = settings.get("GMAIL_CREDENTIALS_FILE")
    if not credentials_file or not os.path.exists(credentials_file):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gmail credentials file not found."
        )

    creds = Credentials.from_authorized_user_file(credentials_file, SCOPES)
    # Refresh credentials if expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Optionally, save the refreshed credentials back to the file.
        with open(credentials_file, "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
    except Exception as e:
        logging.error(f"Failed to build Gmail service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to Gmail API."
        )
    return service


async def fetch_emails(user: str, db: Session = get_db()) -> List[Dict[str, str]]:
    """
    Fetches the latest 10 emails from the Gmail inbox.
    """
    service = get_gmail_service()
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            snippet = msg_data.get('snippet', '')
            emails.append({
                "id": msg['id'],
                "subject": subject,
                "from": sender,
                "snippet": snippet
            })
        return emails
    except Exception as e:
        logging.error(f"Error fetching emails: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch emails from Gmail."
        )


async def draft_reply(emailId: str, user: str) -> str:
    """
    Drafts an email reply by fetching the email content and generating a draft using the LLM.
    """
    service = get_gmail_service()
    try:
        msg_data = service.users().messages().get(userId='me', id=emailId, format='full').execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
        # For simplicity, use the snippet as a proxy for content
        email_content = msg_data.get('snippet', '')
        prompt = f"Draft a concise and professional email reply to the email below.\n\nSubject: {subject}\nFrom: {sender}\nContent: {email_content}\n\nDraft Reply:"
        reply_text = generate_text(prompt)
        if not reply_text:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="LLM could not generate a reply")
        return reply_text
    except Exception as e:
        logging.error(f"Error drafting reply: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to draft reply."
        )


async def send_reply(reply: str, user: str) -> str:
    """
    Sends an email reply via Gmail.
    Constructs a MIME message and uses the Gmail API to send it.
    For demonstration, the sender and recipient are hardcoded; in a real system these should be determined from context.
    """
    service = get_gmail_service()
    # For this example, we use static sender and recipient values.
    sender_email = "me"  # Gmail's 'me' alias
    recipient_email = "recipient@example.com"  # Replace with actual recipient email or determine from context

    mime_message = MIMEText(reply)
    mime_message['to'] = recipient_email
    mime_message['from'] = sender_email
    mime_message['subject'] = "Re: Your Email"  # In a full implementation, derive subject appropriately.
    raw_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode('utf-8')

    try:
        sent_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        return f"Reply sent successfully with message ID: {sent_message['id']}"
    except Exception as e:
        logging.error(f"Error sending reply: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email reply."
        )
