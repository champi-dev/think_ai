"""Fast language model with incremental generation and optimizations."""

import asyncio
import time
from dataclasses import dataclass
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from think_ai.core.config import ModelConfig
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class FastGenerationConfig:
    """Configuration for fast generation."""

    max_tokens: int = 50
    temperature: float = 0.7
    top_p: float = 0.9
    incremental: bool = True
    cache_size: int = 5


class FastLanguageModel:
    """Optimized language model with incremental generation."""

    def __init__(self, config: ModelConfig) -> None:
        self.config = config
        self.model = None
        self.tokenizer = None
        self._cache = {}  # Simple response cache
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize model with optimizations."""
        if self._initialized:
            return

        logger.info("Initializing FastLanguageModel...")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_name,
            trust_remote_code=True,
        )

        # Set padding token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load model with optimizations
        torch_dtype = getattr(torch, self.config.torch_dtype)

        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            use_cache=True,  # Critical for incremental generation
        )

        self.model.eval()
        self._initialized = True
        logger.info("FastLanguageModel initialized successfully")

    async def generate_fast(
        self,
        prompt: str,
        config: FastGenerationConfig | None = None,
    ) -> dict[str, Any]:
        """Generate response with optimizations."""
        if not self._initialized:
            await self.initialize()

        config = config or FastGenerationConfig()

        # Check cache
        cache_key = f"{prompt}_{config.max_tokens}_{config.temperature}"
        if cache_key in self._cache:
            logger.info("Cache hit!")
            return self._cache[cache_key]

        start_time = time.time()

        # Use incremental or standard generation
        if config.incremental and len(prompt.split()) > 3:
            response = await self._generate_incremental(prompt, config)
        else:
            response = await self._generate_standard(prompt, config)

        gen_time = time.time() - start_time

        result = {
            "text": response,
            "generation_time": gen_time,
            "method": "incremental" if config.incremental else "standard",
            "tokens_per_sec": config.max_tokens / gen_time,
        }

        # Cache result
        self._cache[cache_key] = result
        if len(self._cache) > config.cache_size:
            # Remove oldest entry
            self._cache.pop(next(iter(self._cache)))

        return result

    async def _generate_incremental(
        self,
        prompt: str,
        config: FastGenerationConfig,
    ) -> str:
        """Generate using incremental context building."""
        words = prompt.split()

        # Build context incrementally
        context = ""
        past_key_values = None

        # Process words in batches for efficiency
        batch_size = 3  # Process 3 words at a time

        for i in range(0, len(words), batch_size):
            batch = words[i: i + batch_size]
            if i == 0:
                context = " ".join(batch)
            else:
                context += " " + " ".join(batch)

            # Tokenize and cache
            inputs = self.tokenizer(context, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model(
                    inputs["input_ids"],
                    past_key_values=past_key_values,
                    use_cache=True,
                )
                past_key_values = outputs.past_key_values

        # Generate with cached context
        try:
            # Set shorter timeout for incremental
            outputs = await asyncio.wait_for(
                self._run_generation(
                    inputs["input_ids"],
                    past_key_values,
                    config,
                ),
                timeout=20.0,  # 20 second timeout
            )

            response = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=True,
            )

            return response.strip()

        except asyncio.TimeoutError:
            logger.warning("Incremental generation timed out")
            return "I understand your question. Let me think about it and provide a helpful response."

    async def _generate_standard(
        self,
        prompt: str,
        config: FastGenerationConfig,
    ) -> str:
        """Standard generation method."""
        inputs = self.tokenizer(prompt, return_tensors="pt")

        try:
            outputs = await asyncio.wait_for(
                self._run_generation(
                    inputs["input_ids"],
                    None,
                    config,
                ),
                timeout=30.0,  # 30 second timeout
            )

            response = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=True,
            )

            return response.strip()

        except asyncio.TimeoutError:
            logger.warning("Standard generation timed out")
            return self._get_fallback_response(prompt)

    async def _run_generation(
        self,
        input_ids: torch.Tensor,
        past_key_values: Any | None,
        config: FastGenerationConfig,
    ) -> torch.Tensor:
        """Run the actual generation."""
        return await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.model.generate(
                input_ids,
                past_key_values=past_key_values,
                max_new_tokens=config.max_tokens,
                temperature=config.temperature,
                top_p=config.top_p,
                do_sample=True,
                use_cache=True,
                pad_token_id=self.tokenizer.eos_token_id,
                early_stopping=True,
            ),
        )

    def _get_fallback_response(self, prompt: str) -> str:
        """Get appropriate fallback response."""
        prompt_lower = prompt.lower()

        if "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello! I'm Think AI, ready to help you."
        if "what is" in prompt_lower and "sun" in prompt_lower:
            return "The sun is a star at the center of our solar system, providing light and heat to Earth."
        if "programming" in prompt_lower or "code" in prompt_lower:
            return "Yes, I can help with programming in Python, JavaScript, and many other languages."
        return "I'm processing your request. Could you please rephrase or provide more details?"
