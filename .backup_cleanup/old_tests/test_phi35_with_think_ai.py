#!/usr/bin/env python3
"""Test Phi-3.5 Mini integration with Think AI's distributed architecture."""

import asyncio
import time

import httpx


class Phi35ThinkAITest:
    """Test Phi-3.5 Mini with Think AI components."""

    def __init__(self) -> None:
        self.ollama_url = "http://localhost:11434"
        self.stats = {
            "cache_hits": 0,
            "phi35_responses": 0,
            "claude_needed": 0,
            "total_queries": 0,
            "total_time": 0,
            "tokens_generated": 0,
        }

    async def generate_with_phi35(self, prompt: str, context: str = ""):
        """Generate response using Phi-3.5 Mini."""
        full_prompt = f"{context}\n\n{prompt}" if context else prompt

        async with httpx.AsyncClient(timeout=60.0) as client:
            start = time.time()
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "phi3:mini",
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 200,
                    },
                },
            )
            elapsed = time.time() - start

            result = response.json()
            self.stats["tokens_generated"] += result.get("eval_count", 0)

            return {
                "response": result.get("response", ""),
                "confidence": self._calculate_confidence(result),
                "time": elapsed,
                "tokens": result.get("eval_count", 0),
            }

    def _calculate_confidence(self, result):
        """Calculate response confidence (0-1)."""
        # Simplified confidence based on response completeness
        response = result.get("response", "")
        if not response:
            return 0.0

        # Check for complete sentences, code blocks, proper formatting
        confidence = 0.5
        if response.count(".") > 1:
            confidence += 0.2
        if "```" in response or "def " in response:
            confidence += 0.2
        if len(response.split()) > 20:
            confidence += 0.1

        return min(confidence, 1.0)

    async def simulate_think_ai_query(self, query: str):
        """Simulate Think AI's distributed processing with Phi-3.5."""
        start_time = time.time()
        self.stats["total_queries"] += 1

        # 1. Cache check (simulated)
        cache_key = hash(query) % 10
        if cache_key < 3:  # 30% cache hit rate
            self.stats["cache_hits"] += 1
            self.stats["total_time"] += 0.01
            return {
                "source": "cache",
                "response": f"[Cached] Quick answer to: {query}",
                "time": 0.01,
            }

        # 2. Knowledge base context (simulated)
        context = self._get_knowledge_context(query)

        # 3. Generate with Phi-3.5 Mini
        phi35_result = await self.generate_with_phi35(query, context)

        # 4. Check if Claude enhancement needed
        if phi35_result["confidence"] < 0.8 and "complex" in query.lower():
            self.stats["claude_needed"] += 1
            enhanced_response = f"[Claude Enhanced] {phi35_result['response'][:100]}... [enhanced version]"
            total_time = time.time() - start_time
            self.stats["total_time"] += total_time
            return {
                "source": "phi35+claude",
                "response": enhanced_response,
                "time": total_time,
                "confidence": 0.95,
            }

        # 5. Phi-3.5 response is good enough
        self.stats["phi35_responses"] += 1
        total_time = time.time() - start_time
        self.stats["total_time"] += total_time

        return {
            "source": "phi35",
            "response": phi35_result["response"],
            "time": total_time,
            "tokens": phi35_result["tokens"],
            "confidence": phi35_result["confidence"],
        }

    def _get_knowledge_context(self, query) -> str:
        """Simulate knowledge base retrieval."""
        contexts = {
            "consciousness": "Consciousness is awareness of internal and external existence.",
            "fibonacci": "Fibonacci sequence: each number is sum of two preceding ones.",
            "python": "Python is a high-level programming language.",
            "machine learning": "ML is a subset of AI that learns from data.",
            "quantum": "Quantum computing uses quantum mechanics principles.",
        }

        for key, context in contexts.items():
            if key in query.lower():
                return f"Context: {context}"
        return ""

    async def run_test_suite(self) -> None:
        """Run comprehensive test suite."""
        test_queries = [
            "What is consciousness?",
            "Write a Python function to calculate fibonacci numbers",
            "Explain machine learning in simple terms",
            "How does quantum computing work?",
            "What's the weather today?",  # Will need enhancement
            "Solve this complex mathematical proof",  # Will need Claude
            "Tell me about neural networks",
            "How do I reverse a string in Python?",
            "What is the meaning of life?",
            "Explain REST APIs",
        ]

        results = []

        for query in test_queries:
            result = await self.simulate_think_ai_query(query)
            results.append(result)

        # Print statistics

        # Cost calculation
        self.stats["claude_needed"] * 0.015  # $0.015 per Claude query
        self.stats["total_queries"] * 0.015  # If all went to Claude


async def main() -> None:
    """Run the test."""
    tester = Phi35ThinkAITest()
    await tester.run_test_suite()


if __name__ == "__main__":
    asyncio.run(main())
