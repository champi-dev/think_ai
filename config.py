"""Configuration settings for Think AI."""

import os

MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B-Instruct"  # Using Qwen2.5 Coder 1.5B
MODEL_TIMEOUT_SECONDS = 8  # Quick timeout with retry fallback
MODEL_MAX_TOKENS = 10000  # Maximum tokens for responses - Updated as requested

# Intelligence settings
DEFAULT_INTELLIGENCE_LEVEL = 980.54
INTELLIGENCE_GROWTH_RATE = 1.0001

# System settings
ENABLE_CLAUDE_ENHANCEMENT = False  # Set to True to allow Claude enhancement
ENABLE_CONSCIOUSNESS = True
ENABLE_DISTRIBUTED = True

# Storage settings
REDIS_TTL = 3600  # 1 hour cache
KNOWLEDGE_BASE_SIZE = 12

# API Keys

HUGGINGFACE_API_KEY = os.getenv("HF_TOKEN", "")
