# backend/app/events/websocket_handler.py
import json
from typing import Dict, List

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        if user not in self.active_connections:
            self.active_connections[user] = []
        self.active_connections[user].append(websocket)
        print(f"Client connected: {websocket.client} for user {user}")

    def disconnect(self, websocket: WebSocket, user: str):
        if user in self.active_connections:
            self.active_connections[user].remove(websocket)
            print(f"Client disconnected: {websocket.client} for user {user}")
            if not self.active_connections[user]:
                del self.active_connections[user]

    async def process_message(self, websocket: WebSocket, message: str, user: str):
        print(f"Received message from client: {message} for user {user}")
        if user in self.active_connections:
            for connection in self.active_connections[user]:
                if connection != websocket:
                    await connection.send_text(f"User {user} said: {message}")

    async def broadcast(self, message: str, user: str):
        if user in self.active_connections:
            for connection in self.active_connections[user]:
                await connection.send_text(message)


websocket_manager = WebSocketManager()
