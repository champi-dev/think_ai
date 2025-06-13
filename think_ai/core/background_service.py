#!/usr/bin/env python3

"""Background service for Think AI with daemon support."""

import argparse
import asyncio
import json
import logging
import os
import signal
import time
from pathlib import Path

import daemon
import pid

from think_ai.core.think_ai_eternal import ThinkAIEternal
from think_ai.intelligence.self_trainer import SelfTrainingIntelligence as SelfTrainer
from think_ai.storage.manager import StorageManager
from think_ai.utils.logger import setup_logger


class ThinkAIBackgroundService:
    """Manages Think AI as a background service with monitoring capabilities."""

    def __init__(
        self,
        log_file: str = "/var/log/think-ai/core.log",
        pid_file: str = "/var/run/think-ai/core.pid",
    ) -> None:
        self.log_file = Path(log_file)
        self.pid_file = Path(pid_file)
        self.logger = None
        self.think_ai = None
        self.self_trainer = None
        self.running = False
        self.stats = {
            "start_time": time.time(),
            "queries_processed": 0,
            "training_cycles": 0,
            "current_iq": 1000,
            "errors": 0,
        }

    def setup_logging(self) -> None:
        """Configure logging for background service."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.logger = setup_logger(
            name="think_ai_service",
            log_file=str(self.log_file),
            level=logging.INFO,
        )

    def initialize(self) -> None:
        """Initialize Think AI components."""
        try:
            self.logger.info("Initializing Think AI background service...")

            # Initialize storage
            storage_manager = StorageManager()
            storage_manager.initialize()

            # Initialize Think AI
            self.think_ai = ThinkAIEternal()
            self.think_ai.initialize()

            # Initialize self-trainer
            self.self_trainer = SelfTrainer(self.think_ai)

            # Start monitoring thread
            asyncio.create_task(self._monitor_loop())

            # Start health check server
            asyncio.create_task(self._health_check_server())

            self.running = True
            self.logger.info(
                "Think AI background service initialized successfully")

        except Exception as e:
            self.logger.exception(f"Failed to initialize: {e}")
            raise

    async def _monitor_loop(self) -> None:
        """Monitor system health and performance."""
        while self.running:
            try:
                # Update stats
                if self.think_ai:
                    metrics = await self.think_ai.get_intelligence_metrics()
                    self.stats["current_iq"] = metrics.get(
                        "iq", self.stats["current_iq"]
                    )

                # Log stats every 5 minutes
                if int(time.time()) % 300 == 0:
                    self.logger.info(
                        f"Service stats: {
                            json.dumps(
                                self.stats)}"
                    )

                # Write stats to monitoring file
                stats_file = Path("/var/run/think-ai/stats.json")
                stats_file.parent.mkdir(parents=True, exist_ok=True)
                stats_file.write_text(json.dumps(self.stats, indent=2))

                await asyncio.sleep(10)

            except Exception as e:
                self.logger.exception(f"Monitor loop error: {e}")
                self.stats["errors"] += 1

    async def _health_check_server(self) -> None:
        """Simple HTTP health check endpoint."""

        async def handle_health(reader, writer) -> None:
            try:
                request = await reader.read(1024)

                if b"GET /health" in request:
                    response = json.dumps(
                        {
                            "status": "healthy" if self.running else "unhealthy",
                            "uptime": time.time() -
                            self.stats["start_time"],
                            "stats": self.stats,
                        })

                    writer.write(b"HTTP/1.1 200 OK\r\n")
                    writer.write(b"Content-Type: application/json\r\n")
                    writer.write(
                        f"Content-Length: {len(response)}\r\n".encode())
                    writer.write(b"\r\n")
                    writer.write(response.encode())
                else:
                    writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")

                await writer.drain()
                writer.close()

            except Exception as e:
                self.logger.exception(f"Health check error: {e}")

        server = await asyncio.start_server(handle_health, "127.0.0.1", 8888)
        self.logger.info("Health check server started on port 8888")

        async with server:
            await server.serve_forever()

    def handle_signal(self, signum, frame) -> None:
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()

    def shutdown(self) -> None:
        """Gracefully shutdown the service."""
        self.running = False

        if self.self_trainer and self.self_trainer.is_training:
            self.logger.info("Stopping self-training...")
            self.self_trainer.stop_training()

        if self.think_ai:
            self.logger.info("Shutting down Think AI...")
            self.think_ai.shutdown()

        self.logger.info("Service shutdown complete")

    def run_daemon(self) -> None:
        """Run as a daemon process."""
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)

        with daemon.DaemonContext(
            working_directory=os.getcwd(),
            pidfile=pid.TimeoutPIDLockFile(str(self.pid_file)),
            signal_map={
                signal.SIGTERM: self.handle_signal,
                signal.SIGINT: self.handle_signal,
            },
        ):
            self.setup_logging()

            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                loop.run_until_complete(self._run_async())

            except Exception as e:
                if self.logger:
                    self.logger.exception(f"Daemon error: {e}")

    async def _run_async(self) -> None:
        """Async main loop."""
        self.initialize()

        # Start auto-training if configured
        if os.getenv("THINK_AI_AUTO_TRAIN", "false").lower() == "true":
            self.logger.info("Starting auto-training...")
            await self.self_trainer.start_training(
                target_iq=1000000,
                mode="parallel",
            )

        # Keep running
        while self.running:
            await asyncio.sleep(1)

    def run_foreground(self) -> None:
        """Run in foreground (for debugging)."""
        self.setup_logging()

        # Setup signal handlers
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

        try:
            asyncio.run(self._run_async())
        except KeyboardInterrupt:
            self.shutdown()


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Think AI Background Service")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument(
        "--stop",
        action="store_true",
        help="Stop running daemon")
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check daemon status")
    parser.add_argument(
        "--log-file",
        default="/var/log/think-ai/core.log",
        help="Log file path")
    parser.add_argument(
        "--pid-file",
        default="/var/run/think-ai/core.pid",
        help="PID file path")

    args = parser.parse_args()

    service = ThinkAIBackgroundService(
        log_file=args.log_file,
        pid_file=args.pid_file,
    )

    if args.stop:
        # Stop daemon
        if Path(args.pid_file).exists():
            with open(args.pid_file) as f:
                pid_num = int(f.read().strip())
            os.kill(pid_num, signal.SIGTERM)
        else:
            pass

    elif args.status:
        # Check status
        if Path(args.pid_file).exists():
            with open(args.pid_file) as f:
                pid_num = int(f.read().strip())

            try:
                os.kill(pid_num, 0)

                # Try to get stats
                stats_file = Path("/var/run/think-ai/stats.json")
                if stats_file.exists():
                    json.loads(stats_file.read_text())

            except OSError:
                pass
        else:
            pass

    elif args.daemon:
        # Run as daemon
        service.run_daemon()

    else:
        # Run in foreground
        service.run_foreground()


if __name__ == "__main__":
    main()
