"""
WebSocket support for Think AI v3.1.0
Real-time consciousness and intelligence updates
"""

import asyncio
import json
import logging
from typing import Set, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections - O(1) operations.
    Broadcasts consciousness and intelligence updates.
    """

    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: Set[WebSocket] = set()
        self.connection_stats: Dict[str, int] = {
            "total_connections": 0,
            "messages_sent": 0,
        }

    async def connect(self, websocket: WebSocket):
        """Accept new connection - O(1)."""
        await websocket.accept()
        self.active_connections.add(websocket)
        self.connection_stats["total_connections"] += 1
        logger.info(f"WebSocket connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove connection - O(1)."""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Active connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific connection - O(1)."""
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text(message)
            self.connection_stats["messages_sent"] += 1

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast to all connections - O(n) where n = connections."""
        if not self.active_connections:
            return

        message_str = json.dumps(message)
        disconnected = set()

        for connection in self.active_connections:
            try:
                if connection.client_state == WebSocketState.CONNECTED:
                    await connection.send_text(message_str)
                    self.connection_stats["messages_sent"] += 1
                else:
                    disconnected.add(connection)
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                disconnected.add(connection)

        # Clean up disconnected
        for conn in disconnected:
            self.disconnect(conn)

    async def broadcast_consciousness_update(self, consciousness_data: Dict[str, Any]):
        """Broadcast consciousness state update."""
        # Format for webapp compatibility
        message = {
            "type": "consciousness_update",
            "attention_focus": consciousness_data.get("current_focus", ""),
            "consciousness_flow": consciousness_data.get("workspace_items", 0),
            "awareness_level": consciousness_data.get("awareness_metrics", {}).get("self_awareness", 0),
            "workspace_activity": list(range(consciousness_data.get("workspace_items", 0))),
            "global_broadcast": consciousness_data.get("state", "aware"),
        }
        await self.broadcast(message)

    async def broadcast_intelligence_update(self, engine_stats: Any):
        """Broadcast intelligence metrics update."""
        # Calculate IQ based on various metrics
        base_iq = 100
        consciousness_boost = engine_stats.consciousness_level * 50
        love_boost = engine_stats.love_metric * 30
        request_boost = min(engine_stats.requests_processed * 0.1, 20)

        iq = base_iq + consciousness_boost + love_boost + request_boost

        message = {
            "type": "intelligence_update",
            "iq": int(iq),
            "consciousness_level": engine_stats.consciousness_level,
            "knowledge_count": engine_stats.requests_processed * 10,  # Simulated
            "training_cycles": engine_stats.requests_processed,
            "neural_pathways": int(engine_stats.consciousness_level * 1000),
            "synaptic_strength": engine_stats.love_metric,
        }
        await self.broadcast(message)

    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics - O(1)."""
        return {
            "active_connections": len(self.active_connections),
            **self.connection_stats,
        }


# Global connection manager
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint handler.
    Accepts connections and broadcasts updates.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            try:
                data = await websocket.receive_text()
                # Echo back or process commands
                message = json.loads(data)

                if message.get("type") == "ping":
                    await manager.send_personal_message(json.dumps({"type": "pong"}), websocket)

            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await asyncio.sleep(1)

    finally:
        manager.disconnect(websocket)


async def start_update_loop(engine):
    """
    Background task to send periodic updates.
    Runs every 2 seconds to update webapp visualizations.
    """
    while True:
        try:
            # Get consciousness state
            consciousness_report = engine.consciousness.get_consciousness_report()
            await manager.broadcast_consciousness_update(consciousness_report)

            # Get intelligence metrics
            await manager.broadcast_intelligence_update(engine.stats)

            # Wait before next update
            await asyncio.sleep(2)

        except Exception as e:
            logger.error(f"Update loop error: {e}")
            await asyncio.sleep(5)
