# backend/app/services/smart_home.py
from typing import Dict, List

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db
from backend.app.db.models import SmartHomeDevice


async def fetch_devices(
    user: str, db: Session = Depends(get_db)
) -> List[Dict[str, str]]:
    # Placeholder for fetching smart home devices
    devices = db.query(SmartHomeDevice).filter(SmartHomeDevice.user_id == 1).all()
    return [
        {"id": str(device.id), "name": device.name, "status": device.status}
        for device in devices
    ]


async def toggle_device(device_id: str, user: str) -> str:
    # Placeholder for toggling a smart home device
    return f"Toggled device: {device_id}"
