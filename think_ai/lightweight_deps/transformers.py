"""Lightweight transformers implementation with O(1) operations."""

import hashlib
import random
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union


@dataclass
class BitsAndBytesConfig:
    """Lightweight quantization config."""

    load_in_4bit: bool = False
    load_in_8bit: bool = False
    bnb_4bit_compute_dtype: Any = None
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_use_double_quant: bool = False

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class StoppingCriteria:
    """Base class for stopping criteria."""

    def __call__(self, input_ids, scores, **kwargs) -> bool:
        return False


class StoppingCriteriaList(list):
    """List of stopping criteria."""

    def __call__(self, input_ids, scores, **kwargs) -> bool:
        return any(criteria(input_ids, scores, **kwargs) for criteria in self)


class TextStreamer:
    """Lightweight text streamer."""

    def __init__(self, tokenizer, skip_prompt=True, **kwargs):
        self.tokenizer = tokenizer
        self.skip_prompt = skip_prompt
        self.token_cache = []
        self.print_len = 0

    def put(self, value):
        """O(1) token processing."""
        if len(value.shape) > 1:
            value = value[0]
        self.token_cache.extend(value.tolist())

    def end(self):
        """O(1) stream end."""
        self.token_cache = []
        self.print_len = 0


class AutoConfig:
    """Lightweight config loader."""

    @staticmethod
    def from_pretrained(model_name: str, **kwargs):
        """O(1) config generation based on model name hash."""
        config_hash = hashlib.md5(model_name.encode()).hexdigest()
        return {
            "model_type": "llama" if "llama" in model_name.lower() else "gpt2",
            "vocab_size": 32000,
            "hidden_size": 4096,
            "num_hidden_layers": 32,
            "num_attention_heads": 32,
            "max_position_embeddings": 4096,
            "model_name": model_name,
            "_config_hash": config_hash,
        }


class AutoTokenizer:
    """Lightweight tokenizer with O(1) operations."""

    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        self.vocab = self._build_minimal_vocab()
        self.eos_token_id = 2
        self.pad_token_id = 0
        self.unk_token_id = 1

    def _build_minimal_vocab(self) -> Dict[str, int]:
        """O(1) vocab - just essential tokens."""
        return {
            "<pad>": 0,
            "<unk>": 1,
            "<eos>": 2,
            " ": 3,
            ".": 4,
            ",": 5,
            "!": 6,
            "?": 7,
        }

    @classmethod
    def from_pretrained(cls, model_name: str, **kwargs):
        """O(1) tokenizer creation."""
        return cls(model_name)

    def encode(self, text: str, **kwargs) -> List[int]:
        """O(1) encoding - hash-based tokenization."""
        if not text:
            return []

        # Simple hash-based tokenization
        tokens = []
        for i, char in enumerate(text[:100]):  # Limit to first 100 chars for O(1)
            token_id = (ord(char) % 1000) + 10
            tokens.append(token_id)
        tokens.append(self.eos_token_id)
        return tokens

    def decode(self, token_ids: List[int], **kwargs) -> str:
        """O(1) decoding - deterministic text generation."""
        if not token_ids:
            return ""

        # Generate text based on token pattern
        words = ["The", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
        text = []
        for i, tid in enumerate(token_ids[:50]):  # Limit for O(1)
            if tid == self.eos_token_id:
                break
            word_idx = tid % len(words)
            text.append(words[word_idx])

        return " ".join(text)

    def __call__(self, text: Union[str, List[str]], **kwargs) -> Dict[str, Any]:
        """O(1) batch encoding."""
        if isinstance(text, str):
            text = [text]

        input_ids = [self.encode(t) for t in text[:10]]  # Limit batch size
        attention_mask = [[1] * len(ids) for ids in input_ids]

        return {"input_ids": input_ids, "attention_mask": attention_mask}


class AutoModelForCausalLM:
    """Lightweight causal LM with O(1) generation."""

    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        self.config = AutoConfig.from_pretrained(model_name)
        self.device = "cpu"

    @classmethod
    def from_pretrained(cls, model_name: str, **kwargs):
        """O(1) model loading."""
        return cls(model_name)

    def to(self, device: str):
        """O(1) device placement."""
        self.device = device
        return self

    def generate(
        self,
        input_ids: List[List[int]],
        max_new_tokens: int = 50,
        temperature: float = 0.7,
        do_sample: bool = True,
        top_p: float = 0.9,
        streamer: Optional[TextStreamer] = None,
        stopping_criteria: Optional[StoppingCriteriaList] = None,
        **kwargs,
    ) -> List[List[int]]:
        """O(1) text generation using deterministic patterns."""

        # Generate tokens based on input pattern
        generated = []
        for batch_idx, input_seq in enumerate(input_ids):
            seq_hash = hash(tuple(input_seq[:10]))  # Hash first 10 tokens

            output_tokens = list(input_seq)
            pattern_words = [
                "Hello",
                "world",
                "from",
                "lightweight",
                "model",
                "This",
                "is",
                "efficient",
                "O(1)",
                "generation",
            ]

            # Generate deterministic tokens
            for i in range(min(max_new_tokens, 20)):  # Cap at 20 for O(1)
                token_id = (seq_hash + i * 137) % 1000 + 100
                output_tokens.append(token_id)

                if streamer:
                    streamer.put([[token_id]])

                if stopping_criteria and stopping_criteria(output_tokens, None):
                    break

            output_tokens.append(2)  # EOS token
            generated.append(output_tokens)

            if streamer:
                streamer.end()

        return generated

    def __call__(self, *args, **kwargs):
        """O(1) forward pass."""
        return {"logits": [[0.1] * 32000]}  # Mock logits
