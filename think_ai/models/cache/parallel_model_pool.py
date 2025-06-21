"""Parallel model pool for concurrent inference."""

import asyncio
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from think_ai.consciousness.principles import ConstitutionalAI
from think_ai.core.config import ModelConfig
from think_ai.utils.logging import get_logger

from .types import GenerationConfig, ModelInstance, ModelResponse

# Import LanguageModel only for type checking to avoid circular import
if TYPE_CHECKING:
    from .language_model import LanguageModel

logger = get_logger(__name__)


class ParallelModelPool:
    """Pool of language models for parallel processing."""

    def __init__(
        self,
        config: ModelConfig,
        constitutional_ai: ConstitutionalAI | None = None,
        pool_size: int = 3,
    ) -> None:
        self.config = config
        self.constitutional_ai = constitutional_ai
        self.pool_size = pool_size
        self.instances: list[ModelInstance] = []
        self._initialized = False
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize the model pool."""
        if self._initialized:
            return

        logger.info(
            f"Initializing parallel model pool with {
                self.pool_size} instances..."
        )

        # Import LanguageModel here to avoid circular dependency
        from .language_model import LanguageModel

        # Create model instances
        initialization_tasks = []
        for i in range(self.pool_size):
            instance = ModelInstance(
                id=i,
                model=LanguageModel(self.config, self.constitutional_ai),
            )
            self.instances.append(instance)
            initialization_tasks.append(instance.model.initialize())

        # Initialize all models in parallel
        await asyncio.gather(*initialization_tasks)

        self._initialized = True
        logger.info(
            f"Model pool initialized with {len(self.instances)} instances")

    async def get_available_instance(self) -> ModelInstance | None:
        """Get an available model instance."""
        async with self._lock:
            # Find least recently used available instance
            available = [inst for inst in self.instances if not inst.busy]
            if not available:
                return None

            # Sort by last used time
            available.sort(key=lambda x: x.last_used)
            instance = available[0]
            instance.busy = True
            instance.last_used = time.time()
            return instance

    async def release_instance(self, instance: ModelInstance) -> None:
        """Release a model instance back to the pool."""
        async with self._lock:
            instance.busy = False

    async def generate(
        self,
        prompt: str,
        generation_config: GenerationConfig | None = None,
        system_prompt: str | None = None,
        timeout: float = 60.0,
    ) -> ModelResponse:
        """Generate text using an available model instance."""
        # Wait for an available instance
        wait_start = time.time()
        instance = None

        while instance is None:
            instance = await self.get_available_instance()
            if instance is None:
                if time.time() - wait_start > timeout:
                    msg = "No model instance available within timeout"
                    raise TimeoutError(msg)
                await asyncio.sleep(0.1)

        try:
            logger.info(f"Using model instance {instance.id} for generation")
            return await instance.model.generate(
                prompt, generation_config, system_prompt
            )
        finally:
            await self.release_instance(instance)

    async def generate_batch(
        self,
        prompts: list[str],
        generation_config: GenerationConfig | None = None,
        system_prompt: str | None = None,
    ) -> list[ModelResponse]:
        """Generate responses for multiple prompts in parallel."""
        tasks = []
        for prompt in prompts:
            task = self.generate(prompt, generation_config, system_prompt)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions
        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(
                    f"Error generating response for prompt {i}: {result}")
                # Create error response
                responses.append(
                    ModelResponse(
                        text=f"Error: {result!s}",
                        tokens_generated=0,
                        generation_time=0.0,
                        metadata={"error": True},
                    )
                )
            else:
                responses.append(result)

        return responses

    def get_pool_status(self) -> dict[str, Any]:
        """Get current status of the model pool."""
        busy_count = sum(1 for inst in self.instances if inst.busy)
        return {
            "total_instances": len(self.instances),
            "busy_instances": busy_count,
            "available_instances": len(self.instances) - busy_count,
            "initialized": self._initialized,
        }
