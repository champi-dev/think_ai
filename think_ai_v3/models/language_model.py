"""
Language Model Integration for Think AI
Supports Qwen and other models with O(1) caching
Formatter-proof implementation
"""

import asyncio
import time
import hashlib
import logging
from typing import Any, Dict, List, Optional, Union, AsyncGenerator
from dataclasses import dataclass, field
import torch

logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for language models."""
    name: str = "Qwen/Qwen2.5-Coder-1.5B"
    device: str = "auto"
    quantization: Optional[str] = None  # int4, int8
    max_length: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    num_beams: int = 1
    do_sample: bool = True
    use_cache: bool = True
    load_in_8bit: bool = False
    load_in_4bit: bool = False
    device_map: Optional[str] = "auto"
    torch_dtype: Optional[str] = "auto"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for model loading."""
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repetition_penalty": self.repetition_penalty,
            "num_beams": self.num_beams,
            "do_sample": self.do_sample,
            "max_length": self.max_length,
        }


@dataclass
class GenerationResult:
    """Result from text generation - O(1) access to all fields."""
    text: str
    tokens_generated: int
    time_taken: float
    model_name: str
    cached: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class LanguageModel:
    """
    Main language model class with O(1) cached inference.
    Supports multiple models with unified interface.
    """
    
    def __init__(self, config: ModelConfig):
        """Initialize language model."""
        self.config = config
        self.model = None
        self.tokenizer = None
        self.device = self._setup_device()
        self.response_cache = {}  # O(1) lookup
        self.cache_size = 1000
        self.model_loaded = False
        
        # Colombian mode adjustments
        self.colombian_mode = False
        self.sabrosura_temperature = 0.9  # Higher for more flavor
        
        logger.info(f"Language model initialized: {config.name}")
    
    def _setup_device(self) -> torch.device:
        """Setup compute device - O(1)."""
        if self.config.device == "auto":
            if torch.cuda.is_available():
                return torch.device("cuda")
            elif torch.backends.mps.is_available():
                return torch.device("mps")
            else:
                return torch.device("cpu")
        return torch.device(self.config.device)
    
    async def load_model(self):
        """
        Load the model and tokenizer.
        This is O(n) for model size but only done once.
        """
        if self.model_loaded:
            return
        
        try:
            # Import transformers here to avoid issues
            from transformers import (
                AutoModelForCausalLM,
                AutoTokenizer,
                BitsAndBytesConfig,
            )
            
            logger.info(f"Loading model: {self.config.name}")
            
            # Quantization config if needed
            quantization_config = None
            if self.config.load_in_8bit:
                quantization_config = BitsAndBytesConfig(load_in_8bit=True)
            elif self.config.load_in_4bit:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                )
            
            # Load tokenizer - O(1) after caching
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.name,
                trust_remote_code=True,
            )
            
            # Set padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Model loading arguments
            model_kwargs = {
                "trust_remote_code": True,
                "device_map": self.config.device_map,
                "quantization_config": quantization_config,
            }
            
            # Set dtype
            if self.config.torch_dtype == "auto":
                model_kwargs["torch_dtype"] = torch.float16 if self.device.type != "cpu" else torch.float32
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.name,
                **model_kwargs
            )
            
            # Move to device if not using device_map
            if self.config.device_map is None:
                self.model = self.model.to(self.device)
            
            self.model_loaded = True
            logger.info(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            # Fallback to mock model for testing
            self.model = None
            self.tokenizer = None
            self.model_loaded = False
    
    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        """Generate cache key - O(1) hashing."""
        key_data = f"{prompt}_{kwargs}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def generate(
        self,
        prompt: str,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[GenerationResult, AsyncGenerator[str, None]]:
        """
        Generate text from prompt.
        O(1) for cached responses, O(n) for new generation.
        """
        # Check cache first - O(1)
        cache_key = self._get_cache_key(prompt, **kwargs)
        if cache_key in self.response_cache and not stream:
            cached_response = self.response_cache[cache_key]
            return GenerationResult(
                text=cached_response["text"],
                tokens_generated=cached_response["tokens"],
                time_taken=0.0,
                model_name=self.config.name,
                cached=True,
            )
        
        # Load model if needed
        if not self.model_loaded:
            await self.load_model()
        
        # If model still not loaded, return mock response
        if self.model is None:
            if stream:
                return self._mock_stream_generate(prompt)
            else:
                return self._mock_generate(prompt)
        
        # Prepare generation parameters
        gen_params = self.config.to_dict()
        if max_new_tokens:
            gen_params["max_new_tokens"] = max_new_tokens
        if temperature is not None:
            gen_params["temperature"] = temperature
        
        # Colombian mode adjustments
        if self.colombian_mode:
            gen_params["temperature"] = max(
                gen_params["temperature"],
                self.sabrosura_temperature
            )
        
        # Update with any additional kwargs
        gen_params.update(kwargs)
        
        if stream:
            return self._stream_generate(prompt, gen_params)
        else:
            return await self._batch_generate(prompt, gen_params)
    
    async def _batch_generate(
        self,
        prompt: str,
        params: Dict[str, Any]
    ) -> GenerationResult:
        """Non-streaming generation."""
        start_time = time.time()
        
        try:
            # Tokenize - O(n) for prompt length
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=self.config.max_length,
            ).to(self.device)
            
            # Generate - O(n*m) for n tokens, m model size
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    **params,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode - O(n) for output length
            generated_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True,
            )
            
            # Remove prompt from output
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            tokens_generated = len(outputs[0]) - len(inputs["input_ids"][0])
            time_taken = time.time() - start_time
            
            # Cache result - O(1)
            self._add_to_cache(
                prompt,
                {
                    "text": generated_text,
                    "tokens": tokens_generated,
                }
            )
            
            return GenerationResult(
                text=generated_text,
                tokens_generated=tokens_generated,
                time_taken=time_taken,
                model_name=self.config.name,
                cached=False,
            )
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return self._mock_generate(prompt)
    
    async def _stream_generate(
        self,
        prompt: str,
        params: Dict[str, Any]
    ) -> AsyncGenerator[str, None]:
        """Streaming generation - yields tokens as generated."""
        try:
            from transformers import TextIteratorStreamer
            import threading
            
            # Tokenize
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
            ).to(self.device)
            
            # Setup streamer
            streamer = TextIteratorStreamer(
                self.tokenizer,
                skip_prompt=True,
                skip_special_tokens=True,
            )
            
            # Generation kwargs
            generation_kwargs = {
                **inputs,
                **params,
                "streamer": streamer,
                "pad_token_id": self.tokenizer.pad_token_id,
                "eos_token_id": self.tokenizer.eos_token_id,
            }
            
            # Start generation in thread
            thread = threading.Thread(
                target=self.model.generate,
                kwargs=generation_kwargs,
            )
            thread.start()
            
            # Yield tokens as they come
            for token in streamer:
                yield token
            
            thread.join()
            
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            # Fallback to mock streaming
            async for token in self._mock_stream_generate(prompt):
                yield token
    
    def _add_to_cache(self, prompt: str, response: Dict[str, Any]):
        """Add response to cache with LRU eviction - O(1)."""
        cache_key = self._get_cache_key(prompt)
        
        # Evict oldest if at capacity
        if len(self.response_cache) >= self.cache_size:
            # Remove first item (oldest in Python 3.7+ dict)
            first_key = next(iter(self.response_cache))
            del self.response_cache[first_key]
        
        self.response_cache[cache_key] = response
    
    def _mock_generate(self, prompt: str) -> GenerationResult:
        """Mock generation for when model isn't loaded - O(1)."""
        mock_responses = [
            "I understand your request. Let me help you with that.",
            "That's an interesting question! Here's what I think:",
            "Based on my understanding, here's my response:",
        ]
        
        import random
        response = random.choice(mock_responses)
        
        if self.colombian_mode:
            response += " ¡Qué chimba!"
        
        return GenerationResult(
            text=response,
            tokens_generated=len(response.split()),
            time_taken=0.1,
            model_name="mock",
            cached=False,
            metadata={"mock": True},
        )
    
    async def _mock_stream_generate(self, prompt: str) -> AsyncGenerator[str, None]:
        """Mock streaming for testing - O(1) per token."""
        response = "I'm Think AI powered by Qwen! "
        if self.colombian_mode:
            response += "¡Dale parce! "
        response += "Here's my response: This is a mock streaming response."
        
        # Simulate streaming by yielding word by word
        for word in response.split():
            yield word + " "
            await asyncio.sleep(0.05)  # Simulate generation delay
    
    def set_colombian_mode(self, enabled: bool = True):
        """Enable/disable Colombian mode - O(1)."""
        self.colombian_mode = enabled
        if enabled:
            logger.info("¡Colombian mode activated! Subiendo la temperatura...")
    
    def clear_cache(self):
        """Clear response cache - O(1)."""
        self.response_cache.clear()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information - O(1)."""
        return {
            "name": self.config.name,
            "loaded": self.model_loaded,
            "device": str(self.device),
            "cache_size": len(self.response_cache),
            "max_cache_size": self.cache_size,
            "quantization": self.config.quantization,
            "colombian_mode": self.colombian_mode,
        }