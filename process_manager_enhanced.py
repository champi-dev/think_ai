#!/usr/bin/env python3
"""
Enhanced Process Manager for Think AI - orchestrates multiple services with WebSocket support.
Runs API server, webapp, and reverse proxy for Railway deployment.
"""

import asyncio
import logging
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import aiohttp
from aiohttp import web
import urllib.parse

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Check for necessary components
webapp_dir = Path("webapp")
if not webapp_dir.exists():
    logger.error("Webapp directory not found! Please ensure you're in the project root.")
    sys.exit(1)


def start_service(name, command, cwd=None, env=None):
    """Start a service in the background."""
    logger.info(f"Starting {name}...")
    
    process = subprocess.Popen(
        command, cwd=cwd, env=env or os.environ.copy(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Start threads to log output
    def log_output(pipe, prefix):
        for line in iter(pipe.readline, b""):
            logger.info(f"[{prefix}] {line.decode().strip()}")

    threading.Thread(target=log_output, args=(process.stdout, name), daemon=True).start()
    threading.Thread(target=log_output, args=(process.stderr, f"{name}-err"), daemon=True).start()

    return process


async def proxy_handler(request):
    """Handle HTTP requests and proxy them to the appropriate service."""
    path = request.path_qs
    
    # Determine target based on path
    if path.startswith("/api/"):
        # Proxy to API server
        target_url = f"http://localhost:8081{path}"
    else:
        # Proxy to webapp
        target_url = f"http://localhost:3000{path}"
    
    logger.info(f"Proxying {request.method} {path} -> {target_url}")
    
    # Create session and forward request
    async with aiohttp.ClientSession() as session:
        try:
            # Forward the request
            async with session.request(
                method=request.method,
                url=target_url,
                headers={k: v for k, v in request.headers.items() if k.lower() not in ['host', 'connection']},
                data=await request.read() if request.can_read_body else None,
                allow_redirects=False
            ) as resp:
                # Create response
                body = await resp.read()
                response = web.Response(
                    body=body,
                    status=resp.status,
                    headers={k: v for k, v in resp.headers.items() if k.lower() not in ['connection', 'transfer-encoding']}
                )
                return response
        except Exception as e:
            logger.error(f"Proxy error: {e}")
            return web.Response(text=f"Proxy error: {str(e)}", status=502)


async def websocket_handler(request):
    """Handle WebSocket upgrade requests."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    logger.info("WebSocket connection established")
    
    # Connect to backend WebSocket
    session = aiohttp.ClientSession()
    try:
        async with session.ws_connect('ws://localhost:8081/api/v1/ws') as backend_ws:
            
            # Create tasks for bidirectional message forwarding
            async def forward_to_backend():
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        await backend_ws.send_str(msg.data)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error(f'WebSocket error: {ws.exception()}')
                        break
            
            async def forward_to_client():
                async for msg in backend_ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        await ws.send_str(msg.data)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error(f'Backend WebSocket error: {backend_ws.exception()}')
                        break
            
            # Run both forwarding tasks
            await asyncio.gather(forward_to_backend(), forward_to_client())
            
    except Exception as e:
        logger.error(f"WebSocket proxy error: {e}")
    finally:
        await session.close()
        await ws.close()
    
    return ws


async def create_app():
    """Create the aiohttp application."""
    app = web.Application()
    
    # Add routes
    app.router.add_route('*', '/api/v1/ws', websocket_handler)  # WebSocket endpoint
    app.router.add_route('*', '/{path:.*}', proxy_handler)  # Catch-all proxy
    
    return app


async def main():
    """Main entry point."""
    # Get the main port from Railway
    main_port = int(os.environ.get("PORT", "8080"))
    
    logger.info(f"Starting Think AI Full System on Railway port {main_port}")
    
    # Start the API server on internal port 8081
    api_env = os.environ.copy()
    api_env["PORT"] = "8081"
    api_process = start_service("API", [sys.executable, "think_ai_full.py"], env=api_env)
    
    # Wait for API to start
    logger.info("Waiting for API server to start...")
    await asyncio.sleep(5)
    
    # Start the webapp on internal port 3000
    webapp_env = os.environ.copy()
    webapp_env["PORT"] = "3000"
    webapp_env["NODE_ENV"] = "production"
    webapp_env["NEXT_PUBLIC_API_URL"] = "http://localhost:8081"
    
    webapp_process = start_service("Webapp", ["npm", "start"], cwd="webapp", env=webapp_env)
    
    # Wait for webapp to start
    logger.info("Waiting for webapp to start...")
    await asyncio.sleep(10)
    
    # Create and start the reverse proxy
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', main_port)
    await site.start()
    
    logger.info("All services started successfully!")
    logger.info(f"System accessible at: http://0.0.0.0:{main_port}")
    logger.info("WebSocket endpoint: ws://0.0.0.0:{main_port}/api/v1/ws")
    
    # Monitor processes
    try:
        while True:
            # Check if processes are still running
            if api_process.poll() is not None:
                logger.error("API process died!")
                sys.exit(1)
            
            if webapp_process.poll() is not None:
                logger.error("Webapp process died!")
                sys.exit(1)
            
            await asyncio.sleep(5)
    
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        api_process.terminate()
        webapp_process.terminate()
        await runner.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())