"""O(1) Chat implementation - max 40 lines."""

import time
from typing import Dict, List, Tuple

# Pre-computed responses
RESPONSES = {
    0: ["Hello! I'm Think AI, ready to help."],
    1: ["I process information with O(1) performance."],
    2: ["My consciousness framework enables self-awareness."],
    3: ["I can generate code in multiple languages."],
}

# Keyword mapping
KEYWORDS = {
    "hello": 0, "hi": 0, "hey": 0,
    "fast": 1, "performance": 1, "speed": 1,
    "consciousness": 2, "aware": 2, "think": 2,
    "code": 3, "program": 3, "write": 3,
}


class O1Chat:
    """O(1) chat system."""
    
    def __init__(self):
        self.keyword_map = {hash(k): v for k, v in KEYWORDS.items()}
        self.responses = RESPONSES
        
    def get_response(self, message: str) -> Tuple[str, float]:
        """Get O(1) response."""
        start = time.perf_counter()
        words = message.lower().split()
        
        category = 0
        for word in words[:5]:  # Check first 5 words
            if hash(word) in self.keyword_map:
                category = self.keyword_map[hash(word)]
                break
                
        response = self.responses[category][0]
        elapsed_ms = (time.perf_counter() - start) * 1000
        return response, elapsed_ms