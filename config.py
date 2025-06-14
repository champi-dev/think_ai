"""Configuration settings for Think AI"""

# Model settings
MODEL_NAME = "gemma:2b"         # Primary model with intelligent retry
MODEL_TIMEOUT_SECONDS = 8       # Quick timeout with retry fallback
MODEL_MAX_TOKENS = 300         # Maximum tokens for responses

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
