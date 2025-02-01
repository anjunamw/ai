# backend/app/services/finance.py
import os

from fastapi import Depends
from plaid.client import Client
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db


async def get_transactions(user: str, db: Session = Depends(get_db)):
    plaid_client_id = settings.PLAID_CLIENT_ID
    plaid_secret = settings.PLAID_SECRET
    if not plaid_client_id or not plaid_secret:
        return {"message": "Plaid credentials not configured"}

    client = Client(
        client_id=plaid_client_id, secret=plaid_secret, environment="sandbox"
    )  # Use 'sandbox' for testing, 'production' for live data
    try:
        access_token_example = "access-sandbox-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace with a valid Plaid access token (from Plaid Link flow)
        start_date_input = "2024-01-01"
        end_date_input = "2024-02-29"
        response = client.Transactions.get(
            access_token_example, start_date=start_date_input, end_date=end_date_input
        )
        transactions = response["transactions"]
        if transactions:
            return {"message": f"Fetched {len(transactions)} transactions."}
        else:
            return {"message": "No transactions fetched or error occurred."}
    except Exception as e:
        return {"message": f"Error fetching Plaid transactions: {e}"}
