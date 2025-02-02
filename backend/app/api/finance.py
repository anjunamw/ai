# backend/app/api/finance.py
"""
finance.py

Provides an endpoint to fetch simulated finance transactions via the Plaid API.
"""

from fastapi import APIRouter, Depends, HTTPException, status
import logging
from plaid.client import Client
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import TravelResult  # Using TravelResult as a placeholder for finance transactions
from backend.app.core.config import settings

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)


def get_plaid_client():
    client_id = settings.get("PLAID_CLIENT_ID")
    secret = settings.get("PLAID_SECRET")
    if not client_id or not secret:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Plaid credentials missing.")
    try:
        plaid_client = Client(client_id=client_id, secret=secret, environment='sandbox')
        return plaid_client
    except Exception as e:
        logging.error(f"Error initializing Plaid client: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Plaid client initialization failed.")


@router.get("/transactions")
async def get_transactions(user: str, db: Session = Depends(get_db)):
    plaid_client = get_plaid_client()
    # For demo purposes, we assume an access token was obtained via Plaid Link.
    access_token = "access-sandbox-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace with your method to retrieve the token
    try:
        response = plaid_client.Transactions.get(access_token, start_date="2024-01-01", end_date="2024-02-29")
        transactions = response.get('transactions', [])
        # In a real application, transactions should be stored and processed.
        return transactions
    except Exception as e:
        logging.error(f"Error fetching transactions: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch transactions.")
