#!/usr/bin/env python3
"""Start the full Think AI system with both API and webapp."""

import os
import sys
import subprocess
import signal
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Process list to track subprocesses
processes = []

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Shutting down all services...")
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
        except Exception as e:
            logger.error(f"Error terminating process: {e}")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def start_api_server():
    """Start the Think AI API server."""
    logger.info("Starting Think AI API server...")
    
    # Set API port (Railway will use PORT env var, default to 8080)
    api_port = os.environ.get("API_PORT", "8080")
    os.environ["PORT"] = api_port
    
    # Start the API server
    api_process = subprocess.Popen(
        [sys.executable, "start_with_patch.py"],
        env=os.environ.copy()
    )
    processes.append(api_process)
    logger.info(f"API server started on port {api_port}")
    return api_process

def start_webapp():
    """Start the Next.js webapp."""
    logger.info("Starting Next.js webapp...")
    
    # Set webapp port
    webapp_port = os.environ.get("WEBAPP_PORT", "3000")
    
    # Change to webapp directory
    webapp_dir = Path(__file__).parent / "webapp"
    
    # Set environment for production
    webapp_env = os.environ.copy()
    webapp_env["NODE_ENV"] = "production"
    webapp_env["PORT"] = webapp_port
    
    # Start the webapp using npm start (which runs next start)
    webapp_process = subprocess.Popen(
        ["npm", "start"],
        cwd=webapp_dir,
        env=webapp_env
    )
    processes.append(webapp_process)
    logger.info(f"Webapp started on port {webapp_port}")
    return webapp_process

def start_nginx_proxy():
    """Start nginx as a reverse proxy (optional, for Railway we'll use direct ports)."""
    # For Railway, we'll handle routing differently
    # This is a placeholder for local development
    pass

def main():
    """Main entry point."""
    logger.info("Starting Think AI Full System...")
    
    # Determine deployment mode
    is_railway = os.environ.get("RAILWAY_ENVIRONMENT") is not None
    
    if is_railway:
        # On Railway, we need to run on a single port
        # We'll use a process manager or nginx to route traffic
        main_port = os.environ.get("PORT", "8080")
        logger.info(f"Running on Railway with main port: {main_port}")
        
        # Set ports for internal communication
        os.environ["API_PORT"] = "8080"
        os.environ["WEBAPP_PORT"] = "3000"
        
        # We'll need to start a reverse proxy on the main port
        # For now, let's start both services
    else:
        # Local development
        os.environ.setdefault("API_PORT", "8080")
        os.environ.setdefault("WEBAPP_PORT", "3000")
    
    # Start services
    try:
        # Start API server first
        api_process = start_api_server()
        
        # Wait a bit for API to be ready
        time.sleep(5)
        
        # Start webapp
        webapp_process = start_webapp()
        
        # If on Railway, we need a reverse proxy on the main PORT
        if is_railway:
            # We'll handle this in the Dockerfile with a process manager
            pass
        
        logger.info("All services started successfully!")
        logger.info("System is ready:")
        logger.info(f"  - API: http://localhost:{os.environ.get('API_PORT', '8080')}")
        logger.info(f"  - Webapp: http://localhost:{os.environ.get('WEBAPP_PORT', '3000')}")
        
        # Keep running until interrupted
        while True:
            # Check if processes are still running
            for p in processes:
                if p.poll() is not None:
                    logger.error(f"Process {p.pid} has died!")
                    # Restart it or exit
                    signal_handler(None, None)
            
            time.sleep(5)
            
    except Exception as e:
        logger.error(f"Error starting services: {e}")
        signal_handler(None, None)

if __name__ == "__main__":
    main()