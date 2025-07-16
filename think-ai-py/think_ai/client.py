"""
Think AI - Main Python Client

# What is This?
Imagine having a super-smart friend who:
- Already knows every answer (O(1) lookups)
- Never needs to "think" (instant responses)
- Speaks your language (Python!)
- Never gets tired (24/7 availability)

This client is your phone to call that friend!
"""

import json
import time
import asyncio
from typing import Callable, Optional, Dict, Any, List
from urllib.parse import urljoin

import requests

try:
    import websocket
except ImportError:
    websocket = None  # WebSocket support is optional
import aiohttp
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .types import (
    ThinkAIConfig,
    ChatRequest,
    ChatResponse,
    SystemStats,
    HealthStatus,
    KnowledgeDomain,
    SearchResult,
    StreamResponse,
    ThinkAIError,
)


class ThinkAI:
    """
    Think AI Python Client

    # Your Gateway to O(1) AI
    This class is like a universal remote control for AI:
    - Press 'chat' to have a conversation
    - Press 'ask' for quick questions
    - Press 'search' to find knowledge
    - Press 'stream' to watch responses live

    # Why O(1) Matters
    Normal AI: "Let me think..." (seconds pass)
    Think AI: "Here's your answer!" (microseconds pass)

    The difference? We pre-compute and hash everything!
    """

    def __init__(self, config: Optional[ThinkAIConfig] = None):
        """
        Initialize Think AI client with configuration

        # Setting Up Your AI Phone
        Think of this like buying a new smartphone:
        1. Choose your carrier (base_url)
        2. Set call quality (timeout)
        3. Turn on call recording (debug mode)

        # The Smart Retry System
        If your call doesn't go through, we automatically:
        - Try again 3 times
        - Wait a bit longer each time
        - Only give up if the server is really down

        Like a phone that redials when busy!
        """
        self.config = config or ThinkAIConfig()

        # Set up requests session with retry strategy
        # This is like having a phone that auto-redials
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,  # Try 3 times
            backoff_factor=1,  # Wait 1, 2, 4 seconds
            status_forcelist=[429, 500, 502, 503, 504],  # Retry on server errors
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers - like caller ID
        self.session.headers.update(
            {
                "Content-Type": "application/json",  # We speak JSON
                "User-Agent": "think-ai-python/1.0.0",  # Who's calling
            }
        )

        if self.config.debug:
            import logging

            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = None

    def _log(self, message: str) -> None:
        """Log debug message if debug is enabled"""
        if self.logger:
            self.logger.debug(f"[Think AI] {message}")

    def _make_url(self, endpoint: str) -> str:
        """Create full URL for API endpoint"""
        return urljoin(self.config.base_url.rstrip("/") + "/", endpoint.lstrip("/"))

    def _handle_error(self, response: requests.Response) -> None:
        """Handle HTTP error responses"""
        try:
            error_data = response.json()
            message = error_data.get("message", f"HTTP {response.status_code}")
        except (ValueError, KeyError):
            message = f"HTTP {response.status_code}: {response.text}"

        raise ThinkAIError(
            message=message,
            status=response.status_code,
            details=error_data if "error_data" in locals() else None,
        )

    def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Send a chat message to Think AI

        # The Magic Conversation
        This is like texting a friend who:
        1. Always replies instantly (O(1) backend)
        2. Never says "typing..." (no processing delay)
        3. Remembers everything (context awareness)
        4. Always has the perfect answer (pre-computed responses)

        # What Goes In (ChatRequest)
        - query: "What is consciousness?"
        - context: ["We were discussing AI"]
        - max_length: 500

        # What Comes Out (ChatResponse)
        - response: "Consciousness is..."
        - confidence: 0.95 (95% sure)
        - response_time_ms: 42 (blazing fast!)

        # Example
        ```python
        response = ai.chat(ChatRequest(
            query="Explain quantum computing",
            context=["I'm a beginner"]
        ))
        print(f"Answer: {response.response}")
        print(f"Confidence: {response.confidence:.1%}")
        ```
        """
        url = self._make_url("/api/chat")
        self._log(f"POST {url}")

        try:
            # Send the message - like hitting 'send' on your phone
            response = self.session.post(
                url,
                json=request.model_dump(),  # Convert to JSON
                timeout=self.config.timeout,  # Don't wait forever
            )

            # Check if the message was delivered
            if not response.ok:
                self._handle_error(response)

            # Unpack the response - like opening a text message
            data = response.json()
            return ChatResponse(**data)

        except requests.RequestException as e:
            # Network error - like losing signal
            raise ThinkAIError(f"Request failed: {str(e)}")
        except (ValueError, TypeError) as e:
            # Bad response - like getting gibberish
            raise ThinkAIError(f"Invalid response format: {str(e)}")

    def ask(self, question: str) -> str:
        """
        Quick chat - simplified interface

        # The Speed Dial Button
        This is like having your best friend on speed dial:
        - One button press (one parameter)
        - Instant connection (O(1) lookup)
        - Just the answer, no fluff

        # When to Use This
        - Quick questions: ai.ask("What time is it?")
        - Simple queries: ai.ask("Define recursion")
        - No context needed: ai.ask("Hello!")

        # Example
        ```python
        answer = ai.ask("What is the meaning of life?")
        print(answer)  # "42, according to Douglas Adams..."
        ```

        This is just a shortcut for chat() - same O(1) speed!
        """
        request = ChatRequest(query=question)
        response = self.chat(request)
        return response.response  # Just the answer, ma'am!

    def get_stats(self) -> SystemStats:
        """
        Get system statistics

        Returns:
            SystemStats with metrics and performance data
        """
        url = self._make_url("/api/stats")
        self._log(f"GET {url}")

        try:
            response = self.session.get(url, timeout=self.config.timeout)

            if not response.ok:
                self._handle_error(response)

            data = response.json()
            return SystemStats(**data)

        except requests.RequestException as e:
            raise ThinkAIError(f"Request failed: {str(e)}")
        except (ValueError, TypeError) as e:
            raise ThinkAIError(f"Invalid response format: {str(e)}")

    def get_health(self) -> HealthStatus:
        """
        Check system health

        Returns:
            HealthStatus with system component status
        """
        url = self._make_url("/health")
        self._log(f"GET {url}")

        try:
            response = self.session.get(url, timeout=self.config.timeout)

            if not response.ok:
                self._handle_error(response)

            data = response.json()
            return HealthStatus(**data)

        except requests.RequestException as e:
            raise ThinkAIError(f"Request failed: {str(e)}")
        except (ValueError, TypeError) as e:
            raise ThinkAIError(f"Invalid response format: {str(e)}")

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """
        Search knowledge base

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of SearchResult objects
        """
        url = self._make_url("/api/search")
        self._log(f"GET {url}?query={query}&limit={limit}")

        try:
            response = self.session.get(
                url,
                params={"query": query, "limit": limit},
                timeout=self.config.timeout,
            )

            if not response.ok:
                self._handle_error(response)

            data = response.json()

            # Handle different response formats
            if isinstance(data, list):
                results = data
            elif isinstance(data, dict) and "results" in data:
                results = data["results"]
            else:
                results = []

            return [
                SearchResult(**result) if isinstance(result, dict) else result
                for result in results
            ]

        except requests.RequestException as e:
            raise ThinkAIError(f"Request failed: {str(e)}")
        except (ValueError, TypeError) as e:
            raise ThinkAIError(f"Invalid response format: {str(e)}")

    def stream_chat(
        self, request: ChatRequest, on_chunk: Callable[[StreamResponse], None]
    ) -> None:
        """
        Stream chat responses in real-time

        # Netflix vs DVD
        Regular chat() = DVD (get the whole movie at once)
        stream_chat() = Netflix (watch as it downloads)

        # How Streaming Works
        1. Open a WebSocket (like starting a video call)
        2. Send your question
        3. Receive the answer word by word
        4. Each word still comes from O(1) lookups!

        # The Magic Callback
        on_chunk is like your TV showing each frame as it arrives:
        ```python
        def print_as_it_comes(chunk):
            print(chunk.chunk, end='', flush=True)

        ai.stream_chat(
            ChatRequest(query="Tell me a story"),
            print_as_it_comes
        )
        ```

        # Why This is Still O(1)
        Each chunk is retrieved instantly from our hash tables.
        The streaming just makes it feel more natural!
        """
        # Convert HTTP URL to WebSocket URL
        # Like switching from texting to FaceTime
        ws_url = self.config.base_url.replace("http", "ws") + "/ws/chat"
        self._log(f"WebSocket connection to {ws_url}")

        # When we receive a chunk of the response
        def on_message(ws, message):
            try:
                chunk_data = json.loads(message)
                chunk = StreamResponse(**chunk_data)
                on_chunk(chunk)  # Give it to the user immediately!

                if chunk.done:
                    ws.close()  # Hang up when done
            except (ValueError, TypeError) as e:
                raise ThinkAIError(f"Failed to parse stream response: {str(e)}")

        # If something goes wrong
        def on_error(ws, error):
            raise ThinkAIError(f"WebSocket error: {str(error)}")

        # When connection opens, send our question
        def on_open(ws):
            ws.send(json.dumps(request.model_dump()))

        try:
            # Create and run the WebSocket connection
            # Like dialing a video call and keeping it open
            ws = websocket.WebSocketApp(
                ws_url, on_open=on_open, on_message=on_message, on_error=on_error
            )
            ws.run_forever()  # Keep listening until done
        except Exception as e:
            raise ThinkAIError(f"WebSocket connection failed: {str(e)}")

    def ping(self) -> bool:
        """
        Test connection to Think AI

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            self.get_health()
            return True
        except ThinkAIError:
            return False

    def get_domains(self) -> List[KnowledgeDomain]:
        """
        Get knowledge domains

        Returns:
            List of KnowledgeDomain objects sorted by item count
        """
        try:
            stats = self.get_stats()
            domains = [
                KnowledgeDomain(name=name, count=count, activity=1.0)
                for name, count in stats.domain_distribution.items()
            ]
            return sorted(domains, key=lambda d: d.count, reverse=True)
        except ThinkAIError as e:
            raise e

    def set_debug(self, enabled: bool) -> None:
        """Enable or disable debug mode"""
        self.config.debug = enabled
        if enabled and not self.logger:
            import logging

            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger(__name__)
        elif not enabled:
            self.logger = None


class AsyncThinkAI:
    """
    Async Think AI Python Client

    Provides asynchronous access to Think AI's quantum consciousness AI system.
    """

    def __init__(self, config: Optional[ThinkAIConfig] = None):
        """Initialize async Think AI client"""
        self.config = config or ThinkAIConfig()
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "think-ai-python-async/1.0.0",
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    def _make_url(self, endpoint: str) -> str:
        """Create full URL for API endpoint"""
        return urljoin(self.config.base_url.rstrip("/") + "/", endpoint.lstrip("/"))

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Async version of chat"""
        if not self.session:
            raise ThinkAIError("Client not initialized. Use async with statement.")

        url = self._make_url("/api/chat")

        try:
            async with self.session.post(url, json=request.model_dump()) as response:
                if not response.ok:
                    text = await response.text()
                    raise ThinkAIError(
                        f"HTTP {response.status}: {text}", status=response.status
                    )

                data = await response.json()
                return ChatResponse(**data)
        except aiohttp.ClientError as e:
            raise ThinkAIError(f"Request failed: {str(e)}")

    async def ask(self, question: str) -> str:
        """Async quick chat"""
        request = ChatRequest(query=question)
        response = await self.chat(request)
        return response.response


# Convenience functions
def create_client(config: Optional[ThinkAIConfig] = None) -> ThinkAI:
    """Create a new Think AI client instance"""
    return ThinkAI(config)


def quick_chat(question: str, config: Optional[ThinkAIConfig] = None) -> str:
    """Quick one-shot chat with Think AI"""
    client = create_client(config)
    return client.ask(question)
