# backend/app/api/websocket.py
from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from backend.app.core.security import get_current_user
from backend.app.events.websocket_handler import websocket_manager

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, user: str = Depends(get_current_user)
):
    await websocket_manager.connect(websocket, user)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.process_message(websocket, data, user)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, user)
