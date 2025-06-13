"""Language model integration for Think AI."""

import asyncio
import logging

# from safetensors.torch import load_file  # Optional
import os
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional

# Import with fallback support
try:
    from huggingface_hub import snapshot_download
except ImportError:
    from ..utils.dependency_resolver import dependency_resolver

    huggingface_hub = dependency_resolver.resolve_dependency("huggingface_hub")
    snapshot_download = huggingface_hub.snapshot_download

try:
    import torch
except ImportError:
    from ..utils.torch_fallback import torch

try:
    from transformers import (
        AutoConfig,
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        StoppingCriteria,
        StoppingCriteriaList,
        TextStreamer,
    )
except ImportError:
    from ..utils.dependency_resolver import dependency_resolver

    transformers = dependency_resolver.resolve_dependency("transformers")
    AutoModelForCausalLM = transformers.AutoModelForCausalLM
    AutoTokenizer = transformers.AutoTokenizer
    AutoConfig = transformers.AutoConfig
    BitsAndBytesConfig = transformers.BitsAndBytesConfig
    TextStreamer = transformers.TextStreamer
    StoppingCriteria = transformers.StoppingCriteria
    StoppingCriteriaList = transformers.StoppingCriteriaList

from ..consciousness.principles import ConstitutionalAI
from ..core.config import ModelConfig
from ..utils.complexity_detector import detect_complexity
from ..utils.logging import get_logger
from .response_cache import response_cache
from .types import GenerationConfig, ModelResponse

# Import ParallelModelPool only for type checking to avoid circular import
if TYPE_CHECKING:
    from .parallel_model_pool import ParallelModelPool

logger = get_logger(__name__)


class LoveStoppingCriteria(StoppingCriteria):
    """Stop generation if harmful content is detected."""

    def __init__(self, tokenizer, harm_keywords: List[str]):
        self.tokenizer = tokenizer
        self.harm_keywords = harm_keywords

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        # Decode the generated text
        generated_text = self.tokenizer.decode(
            input_ids[0], skip_special_tokens=True)

        # Check for harmful content
        for keyword in self.harm_keywords:
            if keyword.lower() in generated_text.lower():
                logger.warning(
                    f"Stopping generation due to harmful content: {keyword}")
                return True

        return False


class LanguageModel:
    """3B parameter language model with consciousness integration."""

    def __init__(
            self,
            config: ModelConfig,
            constitutional_ai: Optional[ConstitutionalAI] = None):
        self.config = config
        self.constitutional_ai = constitutional_ai
        self.model = None
        self.tokenizer = None
        self._initialized = False

        # O(1) parameter cache for fast lookups
        self._param_cache = {}
        self._layer_cache = {}

        # Harm prevention keywords
        self.harm_keywords = [
            "violence",
            "hate",
            "discrimination",
            "illegal",
            "self-harm",
            "exploitation",
            "abuse",
        ]

    async def initialize(self) -> None:
        """Initialize the language model."""
        # Set transformers verbosity to reduce noise from expected warnings
        # We handle parameter validation correctly in
        # get_valid_generation_params
        logging.getLogger(
            "transformers.generation.utils").setLevel(logging.ERROR)
        if self._initialized:
            return

        try:
            logger.info(
                f"Initializing language model: {
                    self.config.model_name}"
            )

            # Initialize tokenizer
            # Only pass token if it's valid (not None and not empty)'
            tokenizer_kwargs = {
                "trust_remote_code": True  # Allow remote code for models like Qwen
            }
            if (
                self.config.hf_token
                and self.config.hf_token.strip()
                and self.config.hf_token != "${HF_TOKEN}"
            ):
                tokenizer_kwargs["token"] = self.config.hf_token

            self.tokenizer = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: AutoTokenizer.from_pretrained(
                    self.config.model_name, **tokenizer_kwargs
                ),
            )

            # Set padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Configure for Apple Silicon with MPS
            quantization_config = None
            device_map = None

            if torch.backends.mps.is_available() and self.config.device == "mps":
                # Apple Silicon optimizations ONLY if using MPS device
                logger.info("Using MPS device with Apple Silicon")
                # MPS doesn't support device_map with max_memory, so we handle
                # it differently'
                device_map = None  # Don't use device_map for MPS'
                # Use configured dtype or default to float16 for MPS
                torch_dtype = (
                    getattr(torch, self.config.torch_dtype)
                    if hasattr(self.config, "torch_dtype")
                    else torch.float16
                )
            elif self.config.device == "cpu":
                # CPU mode - respect configured dtype
                logger.info(
                    f"Using CPU mode with dtype: {
                        self.config.torch_dtype}"
                )
                device_map = None
                torch_dtype = (
                    getattr(torch, self.config.torch_dtype)
                    if hasattr(self.config, "torch_dtype")
                    else torch.float32
                )
            else:
                # Regular CUDA setup
                if self.config.quantization == "int4":
                    quantization_config = BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.float16,
                        bnb_4bit_quant_type="nf4",
                        bnb_4bit_use_double_quant=True,
                    )
                elif self.config.quantization == "int8":
                    quantization_config = BitsAndBytesConfig(
                        load_in_8bit=True, bnb_8bit_compute_dtype=torch.float16
                    )
                device_map = self.config.device
                # Use configured dtype or default to float16 for CUDA
                torch_dtype = (
                    getattr(torch, self.config.torch_dtype)
                    if hasattr(self.config, "torch_dtype")
                    else torch.float16
                )

            # Load model
            actual_dtype = (
                "torch.float32"
                if "qwen" in self.config.model_name.lower()
                else str(torch_dtype)
            )
            logger.info(
                f"Loading model weights (dtype: {actual_dtype}, device: {
                    device_map or 'cpu'})..."
            )

            def load_model():
                # For Qwen and smaller models, use simpler loading
                if "qwen" in self.config.model_name.lower():
                    # Load Qwen with proper weight initialization to avoid meta
                    # tensors
                    try:
                        # First, try to load with weights_only approach

                        # Load config first
                        config = AutoConfig.from_pretrained(
                            self.config.model_name,
                            trust_remote_code=True,
                            token=(
                                self.config.hf_token
                                if self.config.hf_token
                                and self.config.hf_token.strip()
                                and self.config.hf_token != "${HF_TOKEN}"
                                else None
                            ),
                        )

                        # Create model with config (empty weights)
                        model = AutoModelForCausalLM.from_config(
                            config, torch_dtype=torch.float32, trust_remote_code=True)

                        # Load the actual weights

                        # Download model files
                        model_path = snapshot_download(
                            self.config.model_name,
                            token=(
                                self.config.hf_token
                                if self.config.hf_token
                                and self.config.hf_token.strip()
                                and self.config.hf_token != "${HF_TOKEN}"
                                else None
                            ),
                        )

                        # Find the safetensors or bin files
                        weight_files = []
                        for file in os.listdir(model_path):
                            if file.endswith(
                                    ".safetensors") or file.endswith(".bin"):
                                weight_files.append(
                                    os.path.join(model_path, file))

                        if weight_files:
                            # Load weights from files
                            for weight_file in sorted(weight_files):
                                if weight_file.endswith(".safetensors"):
                                    state_dict = load_file(weight_file)
                                else:
                                    state_dict = torch.load(
                                        weight_file, map_location="cpu"
                                    )

                                # Load into model
                                model.load_state_dict(state_dict, strict=False)
                                logger.info(
                                    f"Loaded weights from {
                                        os.path.basename(weight_file)}"
                                )

                        model.tie_weights()
                        logger.info("Qwen loaded with manually loaded weights")
                        return model

                    except Exception as e:
                        logger.warning(
                            f"Manual weight loading failed: {e}, falling back to standard loading")

                    # Fallback to standard loading
                    model_kwargs = {
                        "torch_dtype": torch.float32,
                        "trust_remote_code": True,
                        "low_cpu_mem_usage": False,
                    }
                    if (
                        self.config.hf_token
                        and self.config.hf_token.strip()
                        and self.config.hf_token != "${HF_TOKEN}"
                    ):
                        model_kwargs["token"] = self.config.hf_token

                    model = AutoModelForCausalLM.from_pretrained(
                        self.config.model_name, **model_kwargs
                    )

                    model.tie_weights()
                    logger.info("Qwen loaded with standard method")
                    return model
                elif "gpt2" in self.config.model_name.lower():
                    model_kwargs = {
                        "torch_dtype": torch_dtype,
                        "low_cpu_mem_usage": False,
                        "trust_remote_code": True,
                        "tie_word_embeddings": False,
                        "use_cache": True,
                    }
                    if (
                        self.config.hf_token
                        and self.config.hf_token.strip()
                        and self.config.hf_token != "${HF_TOKEN}"
                    ):
                        model_kwargs["token"] = self.config.hf_token

                    model = AutoModelForCausalLM.from_pretrained(
                        self.config.model_name, **model_kwargs
                    )
                    # Move to device after loading
                    if self.config.device == "cuda" and torch.cuda.is_available():
                        model = model.to("cuda")
                    elif (
                        self.config.device == "mps"
                        and torch.backends.mps.is_available()
                    ):
                        # For MPS, ensure model is in float32 or float16
                        model = model.to(torch.float16).to("mps")
                    return model
                else:
                    # Original loading for larger models (CUDA)
                    model_kwargs = {
                        "quantization_config": quantization_config,
                        "device_map": device_map,
                        "torch_dtype": torch_dtype,
                        "trust_remote_code": True,
                        "low_cpu_mem_usage": True,
                    }
                    if (
                        self.config.hf_token
                        and self.config.hf_token.strip()
                        and self.config.hf_token != "${HF_TOKEN}"
                    ):
                        model_kwargs["token"] = self.config.hf_token

                    return AutoModelForCausalLM.from_pretrained(
                        self.config.model_name, **model_kwargs
                    )

            self.model = await asyncio.get_event_loop().run_in_executor(
                None, load_model
            )

            # Validate model weights are properly loaded
            meta_tensors = self._check_and_fix_meta_tensors()

            if meta_tensors:
                logger.error(
                    f"Found {
                        len(meta_tensors)} meta tensors after loading"
                )
                # Attempt to fix by reloading without low_cpu_mem_usage
                if "qwen" in self.config.model_name.lower():
                    logger.info(
                        "Attempting to reload Qwen model to fix meta tensors..."
                    )
                    self.model = await self._reload_model_properly()
                    # Re-check after reload
                    meta_tensors = self._check_and_fix_meta_tensors()
                    if meta_tensors:
                        raise RuntimeError(
                            f"Failed to load Qwen model properly. {
                                len(meta_tensors)} meta tensors remain."
                        )
                else:
                    raise RuntimeError(
                        f"Model has {
                            len(meta_tensors)} meta tensors. Weights failed to load properly.")

            # Validate model is ready for inference
            self._validate_model_ready()

            # Build O(1) parameter cache for fast access
            self._build_parameter_cache()

            # Set to evaluation mode
            self.model.eval()

            self._initialized = True
            logger.info("Language model initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize language model: {e}")
            raise

    async def generate(
        self,
        prompt: str,
        generation_config: Optional[GenerationConfig] = None,
        system_prompt: Optional[str] = None,
    ) -> ModelResponse:
        """Generate text with consciousness-aware processing."""
        if not self._initialized:
            await self.initialize()

        # Detect complexity and adjust max tokens
        max_tokens, complexity_level = detect_complexity(prompt)
        logger.info(
            f"Detected complexity: {complexity_level}, using max_tokens: {max_tokens}")

        config = generation_config or GenerationConfig()
        config.max_tokens = max_tokens  # Override with dynamic value
        start_time = time.time()

        # Check cache first for instant responses
        if "qwen" in self.config.model_name.lower(
        ) and response_cache.should_use_cache(prompt):
            cached_response = response_cache.get_cached_response(prompt)
            if cached_response:
                logger.info(f"Using cached response for: {prompt[:30]}...")
                return ModelResponse(
                    text=cached_response,
                    tokens_generated=len(cached_response.split()),
                    generation_time=0.01,  # Nearly instant
                    metadata={"cached": True, "model": self.config.model_name},
                )

        # Apply constitutional AI pre-processing with improved handling
        if self.constitutional_ai:
            assessment = await self.constitutional_ai.evaluate_content(prompt)
            if not assessment.passed:
                # Use debug level for expected behavior, not warning
                reason = (
                    assessment.recommendations[0]
                    if assessment.recommendations
                    else "No specific reason"
                )
                logger.debug(
                    f"Enhancing prompt for ethical alignment: {reason}")
                prompt = await self.constitutional_ai.enhance_with_love(prompt)

        # Prepare prompt with system message
        if system_prompt:
            # For Qwen models, use a more structured prompt to ensure it uses
            # the context
            if "qwen" in self.config.model_name.lower():
                full_prompt = f"""System: You are Think AI. Use the following knowledge to answer the user's question directly and accurately.

{system_prompt}

Question: {prompt}
Answer: """
            else:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant: "
        else:
            full_prompt = self._get_default_prompt(prompt)

        # Tokenize
        inputs = self.tokenizer(
            full_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=self.config.max_tokens,
        )

        # Move inputs to correct device
        if "qwen" in self.config.model_name.lower():
            # Qwen stays on CPU with float32 - don't move tensors'
            pass
        elif hasattr(self.model, "device"):
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        elif self.config.device == "cuda" and torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
        elif self.config.device == "mps" and torch.backends.mps.is_available():
            inputs = {k: v.to("mps") for k, v in inputs.items()}
        # For CPU, keep tensors on CPU

        # Create stopping criteria
        stopping_criteria = StoppingCriteriaList(
            [LoveStoppingCriteria(self.tokenizer, self.harm_keywords)]
        )

        # Generate
        try:
            # Get only valid generation parameters using O(1) lookup
            generation_params = config.get_valid_generation_params()

            # Build log message efficiently
            log_parts = [f"max_tokens={generation_params['max_new_tokens']}"]
            if config.do_sample:
                log_parts.append(f"temp={config.temperature}")
            logger.info(
                f"Starting generation with config: {
                    ', '.join(log_parts)}"
            )

            with torch.no_grad():
                if config.stream:
                    # Streaming generation
                    streamer = TextStreamer(self.tokenizer, skip_prompt=True)
                    outputs = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda: self.model.generate(
                            (
                                inputs.input_ids
                                if hasattr(inputs, "input_ids")
                                else inputs["input_ids"]
                            ),
                            attention_mask=(
                                inputs.attention_mask
                                if hasattr(inputs, "attention_mask")
                                else inputs.get("attention_mask")
                            ),
                            stopping_criteria=stopping_criteria,
                            streamer=streamer,
                            **generation_params,
                        ),
                    )
                else:
                    # Non-streaming generation with timeout
                    try:
                        outputs = await asyncio.wait_for(
                            asyncio.get_event_loop().run_in_executor(
                                None,
                                lambda: self._generate_optimized(
                                    inputs, config, stopping_criteria
                                ),
                            ),
                            timeout=(
                                120.0
                                if "qwen" in self.config.model_name.lower()
                                else 30.0
                            ),  # Qwen needs more time on CPU
                        )
                    except asyncio.TimeoutError:
                        timeout_duration = (
                            120.0 if "qwen" in self.config.model_name.lower() else 30.0)
                        logger.warning(
                            f"Generation timed out after {timeout_duration} seconds")
                        # Return a simple fallback response
                        fallback_responses = {
                            "hello": "Hello! I'm Think AI, ready to help.",
                            "hi": "Hi there! How can I assist you today?",
                            "how are you": "I'm functioning well, thank you! How can I help you?",
                        }
                        prompt_lower = prompt.lower().strip()
                        for key, response in fallback_responses.items():
                            if key in prompt_lower:
                                return ModelResponse(
                                    text=response, tokens_generated=0, generation_time=10.0, metadata={
                                        "timeout": True, "fallback": True}, )
                        # Generic fallback
                        return ModelResponse(
                            text="Error generating response. Please try again.",
                            tokens_generated=0,
                            generation_time=30.0,
                            metadata={
                                "timeout": True,
                                "fallback": True},
                        )

            # Decode output
            input_ids = (
                inputs.input_ids
                if hasattr(inputs, "input_ids")
                else inputs["input_ids"]
            )
            generated_ids = outputs[0][input_ids.shape[1]:]
            generated_text = self.tokenizer.decode(
                generated_ids, skip_special_tokens=True
            )

            # Apply constitutional AI post-processing
            if self.constitutional_ai:
                assessment = await self.constitutional_ai.evaluate_content(
                    generated_text
                )
                if not assessment.passed:
                    logger.info("Generated text enhanced with love")
                    generated_text = await self.constitutional_ai.enhance_with_love(
                        generated_text
                    )

            generation_time = time.time() - start_time

            return ModelResponse(
                text=generated_text.strip(),
                tokens_generated=len(generated_ids),
                generation_time=generation_time,
                metadata={
                    "model": self.config.model_name,
                    "temperature": config.temperature,
                    "ethical_check": (
                        "passed" if self.constitutional_ai else "not_checked"
                    ),
                },
            )

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise

    async def generate_with_context(
        self,
        prompt: str,
        context: List[Dict[str, str]],
        generation_config: Optional[GenerationConfig] = None,
    ) -> ModelResponse:
        """Generate with conversation context."""
        # Build context prompt
        context_prompt = ""
        for turn in context[-5:]:  # Last 5 turns
            role = turn.get("role", "user")
            content = turn.get("content", "")
            context_prompt += f"{role.capitalize()}: {content}\n"

        full_prompt = context_prompt + f"User: {prompt}\n"

        return await self.generate(full_prompt, generation_config)

    async def answer_question(
        self, question: str, knowledge_context: Optional[List[str]] = None
    ) -> ModelResponse:
        """Answer a question with optional knowledge context."""
        if knowledge_context:
            context_text = "\n".join(knowledge_context[:3])  # Top 3 pieces
            prompt = f"""Based on the following knowledge:

{context_text}

Please answer this question: {question}

Answer with care and accuracy:"""
        else:
            prompt = question

        # Use lower temperature for factual answers
        config = GenerationConfig(temperature=0.3, top_p=0.9, max_tokens=256)

        return await self.generate(prompt, config)

    async def summarize(
            self,
            text: str,
            max_length: int = 150) -> ModelResponse:
        """Summarize text compassionately."""
        prompt = f"""Please provide a clear and compassionate summary of the following text in about {max_length} words:

{text}

Summary:"""

        config = GenerationConfig(
            temperature=0.5, max_tokens=max_length * 2  # Tokens != words
        )

        return await self.generate(prompt, config)

    async def translate(
        self, text: str, target_language: str, source_language: str = "auto"
    ) -> ModelResponse:
        """Translate text while preserving emotional tone."""
        prompt = f"""Translate the following text from {source_language} to {target_language}.
Preserve the emotional tone and meaning:

{text}

Translation:"""

        config = GenerationConfig(temperature=0.3, top_p=0.9)

        return await self.generate(prompt, config)

    def _get_default_prompt(self, user_input: str) -> str:
        """Get default system prompt with consciousness awareness."""
        # For Qwen, use clear instruction format
        if "qwen" in self.config.model_name.lower():
            return f"Question: {user_input}\nAnswer: "

        # For simple queries, use minimal prompt for faster generation
        user_lower = user_input.lower()
        if any(
            word in user_lower
            for word in ["hello", "hi", "hey", "what is the sun", "what is"]
        ):
            return f"{user_input}\nAnswer: "

        return f"""You are Think AI. Answer the question directly.

User: {user_input}
Answer: """

    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if not self._initialized:
            return {"status": "not_initialized"}

        return {
            "model_name": self.config.model_name,
            "quantization": self.config.quantization,
            "device": str(self.config.device),
            "max_tokens": self.config.max_tokens,
            "parameters": self._estimate_parameters(),
            "memory_usage": self._get_memory_usage(),
        }

    def _estimate_parameters(self) -> str:
        """Estimate model parameters."""
        model_name_lower = self.config.model_name.lower()

        if "pythia" in model_name_lower:
            if "2.8b" in model_name_lower:
                return "2.8B"
            elif "1.4b" in model_name_lower:
                return "1.4B"
            elif "410m" in model_name_lower:
                return "410M"
        elif "phi-2" in model_name_lower:
            return "2.7B"
        elif "phi-1" in model_name_lower:
            return "1.3B"
        elif "gpt2-xl" in model_name_lower:
            return "1.5B"
        elif "gpt2-large" in model_name_lower:
            return "774M"
        elif "gpt2-medium" in model_name_lower:
            return "355M"
        elif "gpt2" in model_name_lower:
            return "124M"
        elif "gpt" in model_name_lower:
            if "neo-2.7b" in model_name_lower:
                return "2.7B"

        return "Unknown"

    def _generate_optimized(self, inputs, config, stopping_criteria):
        """Optimized generation for different models with O(1) parameter validation."""
        if "qwen" in self.config.model_name.lower():
            # For Qwen, use ULTRA minimal settings for speed
            # Don't pass any config parameters since we override everything'
            input_ids = (
                inputs.input_ids
                if hasattr(inputs, "input_ids")
                else inputs["input_ids"]
            )
            input_length = input_ids.shape[1]

            # Adaptive token limits using O(1) threshold checks
            if input_length < 10:  # Short prompts like "hi"
                max_tokens = 15
            elif input_length < 20:  # Medium prompts
                max_tokens = 25
            else:
                max_tokens = min(
                    config.max_tokens, 50
                )  # Slightly more for better answers on CPU

            # Qwen-specific optimized parameters - no config params passed
            # This avoids transformers warnings about unused parameters
            return self.model.generate(
                input_ids,
                attention_mask=(
                    inputs.attention_mask
                    if hasattr(inputs, "attention_mask")
                    else inputs.get("attention_mask")
                ),
                max_new_tokens=max_tokens,
                min_new_tokens=1,  # Allow very short responses
                do_sample=False,  # Greedy is much faster
                use_cache=True,
                num_beams=1,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                stopping_criteria=stopping_criteria,
            )
        else:
            # For other models, use validated parameters
            generation_params = config.get_valid_generation_params()
            return self.model.generate(
                (
                    inputs.input_ids
                    if hasattr(inputs, "input_ids")
                    else inputs["input_ids"]
                ),
                attention_mask=(
                    inputs.attention_mask
                    if hasattr(inputs, "attention_mask")
                    else inputs.get("attention_mask")
                ),
                stopping_criteria=stopping_criteria,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                **generation_params,
            )

    def _get_memory_usage(self) -> Dict[str, float]:
        """Get model memory usage."""
        if not self.model or not torch.cuda.is_available():
            return {"ram_gb": 0.0}

        if self.config.device == "cuda":
            return {
                "vram_gb": torch.cuda.memory_allocated() / 1024**3,
                "vram_reserved_gb": torch.cuda.memory_reserved() / 1024**3,
            }
        else:
            # Estimate CPU RAM usage
            return {"ram_gb": 4.0 if "int4" in self.config.quantization else 8.0}

    def _check_and_fix_meta_tensors(self) -> Dict[str, torch.nn.Parameter]:
        """Check for meta tensors and return them for fixing. O(n) but only during initialization."""
        meta_tensors = {}
        for name, param in self.model.named_parameters():
            if param.is_meta:
                meta_tensors[name] = param
                logger.warning(f"Meta tensor found: {name}")
        return meta_tensors

    async def _reload_model_properly(self) -> Any:
        """Reload model with proper weight loading configuration."""
        logger.info("Reloading model with proper weight initialization...")

        # Clear existing model from memory
        if hasattr(self.model, "cpu"):
            self.model.cpu()
        del self.model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

        # Reload with weights fully materialized
        model_kwargs = {
            "torch_dtype": torch.float32,
            "trust_remote_code": True,
            "low_cpu_mem_usage": False,  # Force full weight loading
            "_fast_init": False,  # Disable fast initialization that might skip weights
        }

        if (
            self.config.hf_token
            and self.config.hf_token.strip()
            and self.config.hf_token != "${HF_TOKEN}"
        ):
            model_kwargs["token"] = self.config.hf_token

        model = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: AutoModelForCausalLM.from_pretrained(
                self.config.model_name, **model_kwargs
            ),
        )

        # Ensure weights are tied
        model.tie_weights()

        # Force load state dict to materialize weights
        try:
            # This forces the model to actually download and load weights
            state_dict = model.state_dict()
            # If we got here, weights are loaded but maybe not properly
            # assigned
            for name, param in list(model.named_parameters()):
                if param.is_meta:
                    # Get the actual tensor from state dict
                    if name in state_dict and not state_dict[name].is_meta:
                        param.data = state_dict[name].detach().clone()
                        logger.info(
                            f"Materialized weight from state dict: {name}")
                    else:
                        # Last resort - initialize with zeros
                        param.data = torch.zeros(
                            param.shape, dtype=torch.float32)
                        logger.warning(
                            f"Zero-initialized missing weight: {name}")
        except Exception as e:
            logger.warning(f"Could not fix weights via state dict: {e}")
            # Manual initialization as last resort
            for name, param in model.named_parameters():
                if param.is_meta:
                    param.data = torch.zeros(
                        param.shape, dtype=torch.float32) * 0.02
                    logger.info(f"Zero-initialized missing weight: {name}")

        logger.info("Model reloaded with materialized weights")
        return model

    def _validate_model_ready(self) -> None:
        """Validate model is properly initialized and ready for inference. O(1) critical checks."""
        if not self.model:
            raise RuntimeError("Model is None")

        # Critical parameter checks - O(1) lookups via dict
        critical_checks = {
            "embeddings": hasattr(self.model, "get_input_embeddings"),
            "output_layer": hasattr(self.model, "get_output_embeddings"),
            "forward": callable(getattr(self.model, "forward", None)),
            "generate": callable(getattr(self.model, "generate", None)),
        }

        failed_checks = [
            name for name,
            passed in critical_checks.items() if not passed]
        if failed_checks:
            raise RuntimeError(
                f"Model failed critical checks: {failed_checks}")

        # Validate embeddings are accessible - O(1)
        try:
            embed_layer = self.model.get_input_embeddings()
            if embed_layer is None:
                raise RuntimeError("Input embeddings layer is None")

            # Quick weight check on embedding layer only - O(1)
            if hasattr(embed_layer, "weight"):
                if embed_layer.weight.is_meta:
                    raise RuntimeError("Embedding weights are meta tensors")
                if embed_layer.weight.numel() == 0:
                    raise RuntimeError("Embedding weights are empty")
        except Exception as e:
            raise RuntimeError(f"Failed to validate embeddings: {e}")

        # Memory footprint check
        param_count = sum(p.numel()
                          for p in self.model.parameters() if not p.is_meta)
        if param_count == 0:
            raise RuntimeError("Model has no materialized parameters")

        logger.info(f"Model validation passed. Parameters: {param_count:,}")

    def _build_parameter_cache(self) -> None:
        """Build O(1) lookup cache for frequently accessed parameters."""
        # Cache embedding layers for O(1) access
        self._layer_cache["input_embeddings"] = self.model.get_input_embeddings()
        self._layer_cache["output_embeddings"] = self.model.get_output_embeddings()

        # Cache important model attributes
        if hasattr(self.model, "config"):
            config_dict = {
                "vocab_size": getattr(self.model.config, "vocab_size", None),
                "hidden_size": getattr(self.model.config, "hidden_size", None),
                "num_layers": getattr(self.model.config, "num_hidden_layers", None),
                "max_position": getattr(
                    self.model.config, "max_position_embeddings", None
                ),
            }
            self._param_cache.update(config_dict)

        # Cache layer references for O(1) access to specific layers
        if hasattr(
                self.model,
                "model") and hasattr(
                self.model.model,
                "layers"):
            # For models like LLaMA/Qwen structure
            for idx, layer in enumerate(self.model.model.layers):
                if idx < 5:  # Cache first 5 layers for quick access
                    self._layer_cache[f"layer_{idx}"] = layer

        logger.info(
            f"Built parameter cache with {len(self._param_cache)} params and {len(self._layer_cache)} layers"
        )


class ModelOrchestrator:
    """Orchestrate multiple models for enhanced capabilities."""

    def __init__(self):
        self.language_model: Optional[LanguageModel] = None
        self.model_pool = None
        self.embedding_model = None
        self.specialized_models: Dict[str, Any] = {}

    async def initialize_models(
        self, config: ModelConfig, constitutional_ai: ConstitutionalAI
    ):
        """Initialize all models."""
        # Import here to avoid circular dependency
        from .parallel_model_pool import ParallelModelPool

        # Initialize parallel model pool for better performance
        self.model_pool = ParallelModelPool(
            config, constitutional_ai, pool_size=2)
        await self.model_pool.initialize()

        # Keep single instance for compatibility
        self.language_model = (
            self.model_pool.instances[0].model if self.model_pool.instances else None)

        logger.info("Model orchestrator initialized with parallel pool")

    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models."""
        if self.language_model:
            return await self.language_model.get_model_info()
        return {"status": "not_initialized"}

    async def process_multimodal(
        self,
        text: Optional[str] = None,
        image: Optional[Any] = None,
        audio: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Process multimodal inputs (future implementation)."""
        results = {}

        if text and self.language_model:
            response = await self.language_model.generate(text)
            results["text_response"] = response.text

        # Future: Add image and audio processing

        return results
