"""WebSocket connection manager for broadcasting order updates."""

from typing import Set
from fastapi import WebSocket


class ConnectionManager:
    """Manages active WebSocket connections for broadcasting."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Add a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.active_connections.discard(connection)


# Global instance
manager = ConnectionManager()
