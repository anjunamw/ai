# backend/app/services/travel.py
import os
from typing import Dict, List

import requests
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db
from backend.app.db.models import TravelResult


async def search_flights(
    user: str, db: Session = Depends(get_db)
) -> List[Dict[str, str]]:
    SKYSCANNER_API_KEY = settings.SKYSCANNER_API_KEY
    if not SKYSCANNER_API_KEY:
        return []
    url = "https://skyscanner-api.rapidapi.com/v1.0/browsequotes/v1.0/US/USD/en-US/JFK/LAX/2024-03-15"
    headers = {
        "X-RapidAPI-Key": SKYSCANNER_API_KEY,
        "X-RapidAPI-Host": "skyscanner-api.rapidapi.com",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        quotes = data.get("Quotes", [])
        carriers = data.get("Carriers", [])
        places = data.get("Places", [])
        if quotes:
            results = []
            for quote in quotes:
                carrier_ids = quote["OutboundLeg"]["CarrierIds"]
                carrier_names = [
                    carrier["Name"]
                    for carrier in carriers
                    if carrier["CarrierId"] in carrier_ids
                ]
                price = quote["MinPrice"]
                destination_id = quote["OutboundLeg"]["DestinationId"]
                destination_name = next(
                    (
                        place["Name"]
                        for place in places
                        if place["PlaceId"] == destination_id
                    ),
                    "Unknown Destination",
                )
                results.append(
                    {
                        "id": str(quote.get("QuoteId")),
                        "destination": destination_name,
                        "price": price,
                    }
                )
            return results
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error during Skyscanner API request: {e}")
        return []
