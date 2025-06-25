"""HuggingFace provider adapter."""

import asyncio
import time
from typing import Any, AsyncIterator, Dict, List, Optional

from think_ai.models.language.language_model import LanguageModel
from think_ai.models.language.types import GenerationConfig, ModelMetrics, ModelResponse
from think_ai.utils.progress import ModelLoadingProgress

from .base import ModelInfo, ModelProvider


class HuggingFaceProvider(ModelProvider):
    """Provider for HuggingFace Transformers models."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize HuggingFace provider."""
        super().__init__(config)
        self.device = config.get("device", "cpu")
        self.quantization = config.get("quantization", None)
        self.use_cache = config.get("use_cache", True)
        self._model_cache: Dict[str, LanguageModel] = {}

    async def list_models(self) -> List[ModelInfo]:
        """List configured HuggingFace models."""
        # Return a curated list of models that work well
        return [
            ModelInfo(
                name="Qwen/Qwen2.5-0.5B-Instruct",
                provider="huggingface",
                size="0.5B",
                capabilities=["chat", "fast"],
                context_length=32768,
            ),
            ModelInfo(
                name="Qwen/Qwen2.5-1.5B-Instruct",
                provider="huggingface",
                size="1.5B",
                capabilities=["chat"],
                context_length=32768,
            ),
            ModelInfo(
                name="Qwen/Qwen2.5-3B-Instruct",
                provider="huggingface",
                size="3B",
                capabilities=["chat"],
                context_length=32768,
            ),
            ModelInfo(
                name="Qwen/Qwen2.5-7B-Instruct",
                provider="huggingface",
                size="7B",
                capabilities=["chat"],
                context_length=32768,
            ),
            ModelInfo(
                name="Qwen/Qwen2.5-Coder-1.5B-Instruct",
                provider="huggingface",
                size="1.5B",
                capabilities=["coding"],
                context_length=32768,
            ),
            ModelInfo(
                name="Qwen/Qwen2.5-Math-1.5B-Instruct",
                provider="huggingface",
                size="1.5B",
                capabilities=["math"],
                context_length=4096,
            ),
        ]

    async def _get_or_load_model(self, model_name: str) -> LanguageModel:
        """Get a model from cache or load it."""
        if model_name not in self._model_cache:
            # Create config for the model
            from think_ai.core.config import ModelConfig

            model_config = ModelConfig(
                model_name=model_name, device=self.device, quantization=self.quantization, use_cache=self.use_cache
            )

            # Load model with progress indicator
            with ModelLoadingProgress.loading_progress(model_name) as pbar:
                # Load model synchronously in thread pool
                loop = asyncio.get_event_loop()

                # Update progress during loading
                pbar.update(0, "Initializing model...")

                model = await loop.run_in_executor(None, LanguageModel, model_config)

                pbar.update(0, "Model loaded successfully")

            self._model_cache[model_name] = model

        return self._model_cache[model_name]

    async def generate(
        self, model: str, prompt: str, config: GenerationConfig, system_prompt: Optional[str] = None
    ) -> ModelResponse:
        """Generate using HuggingFace model."""
        start_time = time.time()

        try:
            # Get or load the model
            lm = await self._get_or_load_model(model)

            # Run generation in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lm.generate, prompt, config, system_prompt)

            # Add provider info to metrics
            if response.metrics:
                response.metrics.provider = "huggingface"

            return response

        except Exception as e:
            # Return error response
            metrics = ModelMetrics(
                tokens_generated=0,
                generation_time=time.time() - start_time,
                tokens_per_second=0,
                provider="huggingface",
                model=model,
            )

            return ModelResponse(text=f"Error: {str(e)}", metrics=metrics, raw_response={"error": str(e)})

    async def stream_generate(
        self, model: str, prompt: str, config: GenerationConfig, system_prompt: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream generation from HuggingFace model."""
        try:
            # Get or load the model
            lm = await self._get_or_load_model(model)

            # HuggingFace doesn't support true streaming, so we'll generate and yield chunks
            response = await self.generate(model, prompt, config, system_prompt)

            # Yield response in chunks
            chunk_size = 20  # Characters per chunk
            text = response.text

            for i in range(0, len(text), chunk_size):
                yield text[i : i + chunk_size]
                await asyncio.sleep(0.01)  # Small delay to simulate streaming

        except Exception as e:
            yield f"Error: {str(e)}"

    async def is_available(self) -> bool:
        """Check if HuggingFace provider is available."""
        # Always available as it's local
        return True

    def get_provider_name(self) -> str:
        """Get provider name."""
        return "huggingface"

    async def load_model(self, model: str) -> None:
        """Pre-load a model."""
        await self._get_or_load_model(model)

    async def unload_model(self, model: str) -> None:
        """Unload a model from memory."""
        if model in self._model_cache:
            del self._model_cache[model]
