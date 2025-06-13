"""Direct Claude API integration with cost optimization."""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx

from think_ai.consciousness.principles import ConstitutionalAI
from think_ai.persistence.eternal_memory import EternalMemory
from think_ai.utils.logging import get_logger

from .claude_interface import ClaudeInterface

logger = get_logger(__name__)


class ClaudeAPI:
    """Direct Claude API integration with Think AI optimizations.

    Features:
    - Token optimization to minimize costs
    - Automatic response caching
    - Love-aligned filtering
    - Transparent cost tracking
    - Emergency budget protection
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        memory: Optional[EternalMemory] = None,
        ethics: Optional[ConstitutionalAI] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            msg = "Claude API key required. Set CLAUDE_API_KEY environment variable."
            raise ValueError(msg)

        # Configuration from environment
        self.model = os.getenv("CLAUDE_MODEL", "claude-opus-4-20250514")
        self.max_tokens = int(os.getenv("CLAUDE_MAX_TOKENS", "4096"))
        self.cost_per_input_token = float(
            os.getenv("CLAUDE_COST_PER_INPUT_TOKEN", "0.000015")
        )
        self.cost_per_output_token = float(
            os.getenv("CLAUDE_COST_PER_OUTPUT_TOKEN", "0.000075")
        )

        # Features
        self.enabled = os.getenv("CLAUDE_ENABLED", "true").lower() == "true"
        self.budget_limit = float(os.getenv("CLAUDE_BUDGET_LIMIT", "10.0"))
        self.token_optimization = (
            os.getenv("CLAUDE_TOKEN_OPTIMIZATION", "true").lower() == "true"
        )
        self.cache_responses = (
            os.getenv("CLAUDE_CACHE_RESPONSES", "true").lower() == "true"
        )

        # Components
        self.memory = memory
        self.ethics = ethics
        self.interface = ClaudeInterface(
            memory, ethics) if memory and ethics else None

        # Cost tracking
        self.total_cost = 0.0
        self.session_cost = 0.0
        self.request_count = 0

        # Cache
        self.cache_dir = Path.home() / ".think_ai" / "claude_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # HTTP client
        self.client = httpx.AsyncClient(
            timeout=60.0,
            headers={
                "x-api-key": self.api_key,
                "content-type": "application/json",
                "anthropic-version": "2023-06-01",
            },
        )

        logger.info(
            f"Claude API initialized (model: {
                self.model}, budget: ${
                self.budget_limit})"
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()

    async def query(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        optimize_tokens: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Query Claude with optimizations.

        Returns response with cost tracking and ethical filtering.
        """
        if not self.enabled:
            msg = "Claude API is disabled"
            raise ValueError(msg)

        # Check budget
        if self.total_cost >= self.budget_limit:
            msg = f"Budget limit reached: ${
                self.total_cost:.4f} / ${
                self.budget_limit:.2f}"
            raise ValueError(msg)

        # Apply token optimization if enabled
        if optimize_tokens is None:
            optimize_tokens = self.token_optimization

        if optimize_tokens and self.interface:
            optimized_prompt, optimization_report = (
                await self.interface.create_optimized_prompt(prompt)
            )
            prompt = optimized_prompt
            logger.info(
                f"Token optimization: {
                    optimization_report['reduction_percentage']:.1f}% reduction")

        # Check cache first
        if self.cache_responses:
            cached_response = await self._check_cache(prompt)
            if cached_response:
                logger.info("Using cached Claude response")
                return {
                    "response": cached_response["content"],
                    "source": "cache",
                    "cost": 0.0,
                    "cached": True,
                    "original_cost": cached_response.get("cost", 0.0),
                }

        # Prepare request
        messages = [{"role": "user", "content": prompt}]

        # Add system message if provided
        request_data = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature,
            "messages": messages,
        }

        if system:
            request_data["system"] = system

        # Estimate cost before request
        estimated_cost = await self._estimate_cost(
            prompt, max_tokens or self.max_tokens
        )

        if self.total_cost + estimated_cost > self.budget_limit:
            logger.warning(
                f"Request would exceed budget: ${
                    estimated_cost:.4f} (remaining: ${
                    self.budget_limit -
                    self.total_cost:.4f})"
            )
            return await self._suggest_alternatives(prompt)

        try:
            # Make API request
            logger.info(
                f"Calling Claude API (estimated cost: ${
                    estimated_cost:.4f})"
            )

            response = await self.client.post(
                "https://api.anthropic.com/v1/messages",
                json=request_data,
            )

            response.raise_for_status()
            result = response.json()

            # Extract response content
            content = ""
            if result.get("content") and len(result["content"]) > 0:
                content = result["content"][0].get("text", "")

            # Calculate actual cost
            usage = result.get("usage", {})
            input_tokens = usage.get("input_tokens", 0)
            output_tokens = usage.get("output_tokens", 0)

            actual_cost = (
                input_tokens * self.cost_per_input_token
                + output_tokens * self.cost_per_output_token
            )

            # Update cost tracking
            self.total_cost += actual_cost
            self.session_cost += actual_cost
            self.request_count += 1

            # Ethical filtering if available
            if self.ethics and content:
                assessment = await self.ethics.evaluate_content(content)
                if not assessment.passed:
                    logger.warning("Claude response failed ethical review")
                    content = await self._apply_love_filter(content, assessment)

            # Cache response
            if self.cache_responses:
                await self._cache_response(prompt, content, actual_cost, result)

            # Log to eternal memory
            if self.memory:
                await self.memory.save_conversation(
                    f"claude_api_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    [
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": content},
                    ],
                    {
                        "api_call": True,
                        "cost": actual_cost,
                        "tokens": usage,
                        "model": self.model,
                    },
                )

            logger.info(
                f"Claude response received (cost: ${
                    actual_cost:.4f}, tokens: {input_tokens}→{output_tokens})"
            )

            return {
                "response": content,
                "source": "claude_api",
                "cost": actual_cost,
                "tokens": usage,
                "model": self.model,
                "cached": False,
                "ethical_review": assessment.passed if self.ethics else True,
            }

        except httpx.HTTPStatusError as e:
            logger.exception(
                f"Claude API error: {e.response.status_code} - {e.response.text}"
            )

            if e.response.status_code == 429:
                # Rate limited - suggest waiting
                return {
                    "error": "rate_limited",
                    "message": "Claude API rate limit reached. Please wait before trying again.",
                    "retry_after": e.response.headers.get(
                        "retry-after",
                        "60"),
                }
            if e.response.status_code == 400:
                # Bad request - likely token limit
                return await self._handle_token_limit_error(prompt)
            raise

        except Exception as e:
            logger.exception(f"Unexpected Claude API error: {e}")
            return await self._suggest_alternatives(prompt)

    async def query_with_conversation(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query Claude with full conversation context."""
        # Optimize conversation for tokens
        if self.token_optimization and self.interface:
            optimized_messages = await self._optimize_conversation(messages)
        else:
            optimized_messages = messages

        request_data = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "messages": optimized_messages,
        }

        if system:
            request_data["system"] = system

        # Similar to query() but with conversation context
        try:
            response = await self.client.post(
                "https://api.anthropic.com/v1/messages",
                json=request_data,
            )

            response.raise_for_status()
            result = response.json()

            # Process similar to query()
            content = ""
            if result.get("content") and len(result["content"]) > 0:
                content = result["content"][0].get("text", "")

            usage = result.get("usage", {})
            cost = (
                usage.get("input_tokens", 0) * self.cost_per_input_token
                + usage.get("output_tokens", 0) * self.cost_per_output_token
            )

            self.total_cost += cost

            return {
                "response": content,
                "cost": cost,
                "tokens": usage,
                "model": self.model,
            }

        except Exception as e:
            logger.exception(f"Conversation query error: {e}")
            raise

    def get_cost_summary(self) -> Dict[str, Any]:
        """Get cost tracking summary."""
        return {
            "total_cost": self.total_cost,
            "session_cost": self.session_cost,
            "budget_limit": self.budget_limit,
            "budget_used_percentage": (
                (self.total_cost / self.budget_limit * 100)
                if self.budget_limit > 0
                else 0
            ),
            "request_count": self.request_count,
            "average_cost_per_request": (
                self.total_cost / self.request_count if self.request_count > 0 else 0
            ),
            "budget_remaining": max(0, self.budget_limit - self.total_cost),
        }

    async def _estimate_cost(self, prompt: str, max_tokens: int) -> float:
        """Estimate cost before making request."""
        # Rough estimation: 4 chars per token
        estimated_input_tokens = len(prompt) // 4
        estimated_output_tokens = min(max_tokens, 500)  # Conservative estimate

        return (
            estimated_input_tokens * self.cost_per_input_token
            + estimated_output_tokens * self.cost_per_output_token
        )

    async def _check_cache(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Check if prompt has cached response."""
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        cache_file = self.cache_dir / f"{prompt_hash}.json"

        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    cached = json.load(f)

                # Check if cache is still fresh (24 hours)
                cache_time = datetime.fromisoformat(cached["timestamp"])
                if (datetime.now() - cache_time).total_seconds() < 86400:
                    return cached

            except Exception as e:
                logger.warning(f"Error reading cache: {e}")

        return None

    async def _cache_response(
        self,
        prompt: str,
        content: str,
        cost: float,
        full_response: Dict[str, Any],
    ) -> None:
        """Cache Claude response."""
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        cache_file = self.cache_dir / f"{prompt_hash}.json"

        try:
            cache_data = {
                "prompt": prompt,
                "content": content,
                "cost": cost,
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "usage": full_response.get("usage", {}),
            }

            with open(cache_file, "w") as f:
                json.dump(cache_data, f, indent=2)

        except Exception as e:
            logger.warning(f"Error caching response: {e}")

    async def _suggest_alternatives(self, prompt: str) -> dict[str, Any]:
        """Suggest free alternatives when API fails or budget exceeded."""
        if self.interface:
            alternatives = await self.interface.prepare_claude_alternatives(prompt)
            return {
                "error": "api_unavailable",
                "message": "Claude API unavailable - free alternatives suggested",
                "alternatives": alternatives,
                "fallback_available": True,
            }

        return {
            "error": "api_unavailable",
            "message": "Claude API unavailable and no alternatives configured",
            "fallback_available": False,
        }

    async def _handle_token_limit_error(self, prompt: str) -> dict[str, Any]:
        """Handle token limit exceeded error."""
        if self.interface:
            # Try to compress the prompt more aggressively
            compressed_prompt = await self.interface._compress_text(prompt)
            if len(compressed_prompt) < len(prompt) * \
                    0.7:  # Significant reduction
                return {
                    "error": "token_limit",
                    "message": "Prompt too long - try this compressed version",
                    "compressed_prompt": compressed_prompt,
                    "reduction": f"{((len(prompt) - len(compressed_prompt)) / len(prompt) * 100):.1f}%",
                }

        return {
            "error": "token_limit",
            "message": "Prompt exceeds token limit - please shorten your request",
            "original_length": len(prompt),
            "max_recommended": self.max_tokens * 3,  # Rough chars estimate
        }

    async def _apply_love_filter(
        self,
        content: str,
        assessment: Any,
    ) -> str:
        """Apply love-based filtering to response."""
        # Add love-aligned preamble
        return (
            "⚠️  Original response was filtered for love alignment.\n\n"
            f"**Concerns**: {', '.join(assessment.concerns)}\n\n"
            f"**Love-Aligned Response**: {content}\n\n"
            f"**Recommendations**: {', '.join(assessment.recommendations)}"
        )

    async def _optimize_conversation(
        self,
        messages: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        """Optimize conversation messages for token efficiency."""
        if not self.interface:
            return messages

        optimized = []
        for msg in messages:
            if msg["role"] == "user":
                # Compress user messages
                compressed_content = await self.interface._compress_text(msg["content"])
                optimized.append(
                    {
                        "role": "user",
                        "content": compressed_content,
                    }
                )
            else:
                # Keep assistant messages as-is but truncate if very long
                content = msg["content"]
                # Keep full content, don't truncate assistant messages
                # Token optimization should happen at prompt level, not
                # response level
                optimized.append(
                    {
                        "role": "assistant",
                        "content": content,
                    }
                )

        return optimized


# Utility function for easy API access
async def create_claude_api(
    memory: Optional[EternalMemory] = None,
    ethics: Optional[ConstitutionalAI] = None,
) -> ClaudeAPI:
    """Create Claude API instance with Think AI integration."""
    return ClaudeAPI(memory=memory, ethics=ethics)
