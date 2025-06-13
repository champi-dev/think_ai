#!/usr/bin/env python3

"""Bridge module for Go API server to communicate with Think AI."""

import asyncio
import json
import sys
from typing import Any

from think_ai.coding.code_generator import CodeGenerator
from think_ai.core.think_ai_eternal import ThinkAIEternal
from think_ai.intelligence.self_trainer import SelfTrainer
from think_ai.storage.manager import StorageManager


class ThinkAIBridge:
    """Handles JSON-RPC style communication between Go server and Think AI."""

    def __init__(self) -> None:
        self.think_ai = None
        self.code_generator = None
        self.self_trainer = None
        self.storage_manager = None
        self._initialize()

    def _initialize(self) -> None:
        """Initialize Think AI components."""
        try:
            self.storage_manager = StorageManager()
            self.storage_manager.initialize()

            self.think_ai = ThinkAIEternal()
            self.think_ai.initialize()

            self.code_generator = CodeGenerator()
            self.self_trainer = SelfTrainer(self.think_ai)

        except Exception as e:
            self._send_error(None, -32603, f"Initialization failed: {e!s}")
            sys.exit(1)

    def _send_response(self, request_id: str, result: Any) -> None:
        """Send successful response."""

    def _send_error(self, request_id: str, code: int, message: str) -> None:
        """Send error response."""

    async def handle_request(self, request: dict[str, Any]) -> None:
        """Handle incoming request from Go server."""
        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "think":
                result = await self._handle_think(params)
            elif method == "generate_code":
                result = await self._handle_generate_code(params)
            elif method == "get_intelligence":
                result = await self._handle_get_intelligence()
            elif method == "start_training":
                result = await self._handle_start_training(params)
            elif method == "stop_training":
                result = await self._handle_stop_training()
            elif method == "get_training_status":
                result = await self._handle_get_training_status()
            elif method == "store_knowledge":
                result = await self._handle_store_knowledge(params)
            elif method == "search_knowledge":
                result = await self._handle_search_knowledge(params)
            elif method == "get_consciousness_state":
                result = await self._handle_get_consciousness_state()
            else:
                self._send_error(
                    request_id, -32601, f"Method not found: {method}")
                return

            self._send_response(request_id, result)

        except Exception as e:
            self._send_error(request_id, -32603, str(e))

    async def _handle_think(self, params: dict[str, Any]) -> dict[str, Any]:
        """Handle think request."""
        query = params.get("query", "")
        context = params.get("context", {})
        temperature = params.get("temperature", 0.7)
        max_tokens = params.get("max_tokens", 5000)
        enable_consciousness = params.get("consciousness", True)

        response = await self.think_ai.think(
            query=query,
            context=context,
            temperature=temperature,
            max_tokens=max_tokens,
            use_consciousness=enable_consciousness,
        )

        return {
            "response": response.content,
            "tokens_used": response.tokens_used,
            "consciousness_state": (
                response.consciousness_state if enable_consciousness else None
            ),
            "reasoning_path": response.reasoning_path,
        }

    async def _handle_generate_code(
            self, params: dict[str, Any]) -> dict[str, Any]:
        """Handle code generation request."""
        prompt = params.get("prompt", "")
        language = params.get("language", "python")
        paradigm = params.get("paradigm", "object-oriented")
        complexity = params.get("complexity", 5)

        code = await self.code_generator.generate(
            prompt=prompt,
            language=language,
            paradigm=paradigm,
            complexity_level=complexity,
        )

        return {
            "code": code,
            "language": language,
            "paradigm": paradigm,
            "complexity": complexity,
        }

    async def _handle_get_intelligence(self) -> dict[str, Any]:
        """Get current intelligence metrics."""
        return await self.think_ai.get_intelligence_metrics()

    async def _handle_start_training(
            self, params: dict[str, Any]) -> dict[str, Any]:
        """Start self-training process."""
        mode = params.get("mode", "parallel")
        target_iq = params.get("target_iq", 1000000)
        parallel_tests = params.get("parallel_tests", 5)

        training_id = await self.self_trainer.start_training(
            target_iq=target_iq,
            mode=mode,
            parallel_tests=parallel_tests,
        )

        return {
            "training_id": training_id,
            "status": "started",
        }

    async def _handle_stop_training(self) -> dict[str, Any]:
        """Stop self-training process."""
        stopped = await self.self_trainer.stop_training()
        return {"stopped": stopped}

    async def _handle_get_training_status(self) -> dict[str, Any]:
        """Get training status."""
        return await self.self_trainer.get_status()

    async def _handle_store_knowledge(
            self, params: dict[str, Any]) -> dict[str, Any]:
        """Store knowledge in the system."""
        concept = params.get("concept", "")
        content = params.get("content", "")
        category = params.get("category", "general")
        metadata = params.get("metadata", {})

        stored = await self.storage_manager.store_knowledge(
            concept=concept,
            content=content,
            category=category,
            metadata=metadata,
        )

        return {"stored": stored}

    async def _handle_search_knowledge(
            self, params: dict[str, Any]) -> dict[str, Any]:
        """Search knowledge base."""
        query = params.get("query", "")
        limit = params.get("limit", 10)

        results = await self.storage_manager.search_knowledge(
            query=query,
            limit=limit,
        )

        return {"results": results}

    async def _handle_get_consciousness_state(self) -> dict[str, Any]:
        """Get current consciousness state."""
        state = self.think_ai.consciousness.get_current_state()
        return state.to_dict()

    async def run(self) -> None:
        """Main loop reading from stdin and processing requests."""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None,
                    sys.stdin.readline,
                )

                if not line:
                    break

                request = json.loads(line.strip())
                await self.handle_request(request)

            except json.JSONDecodeError as e:
                self._send_error(None, -32700, f"Parse error: {e!s}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                self._send_error(None, -32603, f"Internal error: {e!s}")


def main() -> None:
    """Main entry point."""
    bridge = ThinkAIBridge()
    asyncio.run(bridge.run())


if __name__ == "__main__":
    main()
