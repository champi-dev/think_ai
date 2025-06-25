#!/usr/bin/env python3
"""
WebSocket proxy server for Think AI.
Runs alongside the main reverse proxy to handle WebSocket connections.
"""

import asyncio
import json
import logging
import sys

import websockets

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def forward_messages(client_ws, backend_ws):
    """Forward messages between client and backend WebSocket."""
    try:
        async for message in client_ws:
            logger.debug(f"Client -> Backend: {message}")
            await backend_ws.send(message)
    except websockets.exceptions.ConnectionClosed:
        logger.info("Client WebSocket closed")
    except Exception as e:
        logger.error(f"Error forwarding from client: {e}")


async def backward_messages(client_ws, backend_ws):
    """Forward messages from backend to client WebSocket."""
    try:
        async for message in backend_ws:
            logger.debug(f"Backend -> Client: {message}")
            await client_ws.send(message)
    except websockets.exceptions.ConnectionClosed:
        logger.info("Backend WebSocket closed")
    except Exception as e:
        logger.error(f"Error forwarding from backend: {e}")


async def handle_websocket(websocket, path):
    """Handle incoming WebSocket connections."""
    logger.info(f"New WebSocket connection from {websocket.remote_address}")

    # Connect to backend WebSocket
    backend_uri = "ws://localhost:8081/api/v1/ws"

    try:
        async with websockets.connect(backend_uri) as backend_ws:
            logger.info("Connected to backend WebSocket")

            # Create tasks for bidirectional message forwarding
            forward_task = asyncio.create_task(forward_messages(websocket, backend_ws))
            backward_task = asyncio.create_task(backward_messages(websocket, backend_ws))

            # Wait for either task to complete
            done, pending = await asyncio.wait([forward_task, backward_task], return_when=asyncio.FIRST_COMPLETED)

            # Cancel pending tasks
            for task in pending:
                task.cancel()

    except Exception as e:
        logger.error(f"WebSocket proxy error: {e}")
        # Send error message to client
        try:
            await websocket.send(json.dumps({"type": "error", "message": f"Backend connection failed: {str(e)}"}))
        except:
            pass

    finally:
        logger.info("WebSocket connection closed")


async def main():
    """Start the WebSocket proxy server."""
    port = 8082  # Internal port for WebSocket proxy

    logger.info(f"Starting WebSocket proxy on port {port}")

    async with websockets.serve(handle_websocket, "0.0.0.0", port):
        logger.info(f"WebSocket proxy listening on ws://0.0.0.0:{port}")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("WebSocket proxy shutting down...")
        sys.exit(0)
