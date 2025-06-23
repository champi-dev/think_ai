"""Ollama provider for language models."""

import json
import time
from typing import List, Dict, Any, Optional, AsyncIterator
from urllib.parse import urljoin
import asyncio
from dataclasses import dataclass
import aiohttp

from .base import ModelProvider, ModelInfo
from think_ai.models.language.types import GenerationConfig, ModelResponse, ModelMetrics


class OllamaProvider(ModelProvider):
    """Provider for Ollama-hosted models."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Ollama provider.
        
        Args:
            config: Configuration with 'base_url' (default: http://localhost:11434)
        """
        super().__init__(config)
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.timeout = config.get('timeout', 60)
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session
    
    async def list_models(self) -> List[ModelInfo]:
        """List available models from Ollama."""
        try:
            session = await self._get_session()
            url = urljoin(self.base_url, '/api/tags')
            
            async with session.get(url) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
                models = []
                
                for model_data in data.get('models', []):
                    name = model_data['name']
                    
                    # Determine capabilities based on model name
                    capabilities = []
                    name_lower = name.lower()
                    
                    if 'qwen' in name_lower:
                        if 'coder' in name_lower:
                            capabilities.append('coding')
                        elif 'math' in name_lower:
                            capabilities.append('math')
                        elif 'vl' in name_lower or 'vision' in name_lower:
                            capabilities.append('multimodal')
                        else:
                            capabilities.append('chat')
                    
                    # Extract size from name
                    size = None
                    if 'b' in name_lower:
                        parts = name_lower.split('-')
                        for part in parts:
                            if part.endswith('b'):
                                size = part
                                break
                    
                    models.append(ModelInfo(
                        name=name,
                        provider='ollama',
                        size=size,
                        capabilities=capabilities,
                        context_length=model_data.get('details', {}).get('parameter_size', 4096)
                    ))
                
                return models
                
        except Exception as e:
            print(f"Error listing Ollama models: {e}")
            return []
    
    async def generate(
        self,
        model: str,
        prompt: str,
        config: GenerationConfig,
        system_prompt: Optional[str] = None
    ) -> ModelResponse:
        """Generate a response from an Ollama model."""
        start_time = time.time()
        
        try:
            session = await self._get_session()
            url = urljoin(self.base_url, '/api/generate')
            
            # Build the full prompt with system message if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
            
            payload = {
                'model': model,
                'prompt': full_prompt,
                'stream': False,
                'options': {
                    'temperature': config.temperature,
                    'top_p': config.top_p,
                    'top_k': config.top_k,
                    'num_predict': config.max_tokens,
                    'stop': config.stop_sequences or []
                }
            }
            
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error: {error_text}")
                
                data = await response.json()
                generation_time = time.time() - start_time
                
                # Extract token counts if available
                eval_count = data.get('eval_count', 0)
                prompt_eval_count = data.get('prompt_eval_count', 0)
                
                metrics = ModelMetrics(
                    tokens_generated=eval_count,
                    generation_time=generation_time,
                    tokens_per_second=eval_count / generation_time if generation_time > 0 else 0,
                    provider='ollama',
                    model=model
                )
                
                return ModelResponse(
                    text=data['response'],
                    metrics=metrics,
                    raw_response=data
                )
                
        except Exception as e:
            # Return error response
            metrics = ModelMetrics(
                tokens_generated=0,
                generation_time=time.time() - start_time,
                tokens_per_second=0,
                provider='ollama',
                model=model
            )
            
            return ModelResponse(
                text=f"Error: {str(e)}",
                metrics=metrics,
                raw_response={'error': str(e)}
            )
    
    async def stream_generate(
        self,
        model: str,
        prompt: str,
        config: GenerationConfig,
        system_prompt: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream generation from an Ollama model."""
        try:
            session = await self._get_session()
            url = urljoin(self.base_url, '/api/generate')
            
            # Build the full prompt with system message if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
            
            payload = {
                'model': model,
                'prompt': full_prompt,
                'stream': True,
                'options': {
                    'temperature': config.temperature,
                    'top_p': config.top_p,
                    'top_k': config.top_k,
                    'num_predict': config.max_tokens,
                    'stop': config.stop_sequences or []
                }
            }
            
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    yield f"Error: {error_text}"
                    return
                
                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line)
                            if 'response' in data:
                                yield data['response']
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            yield f"Error: {str(e)}"
    
    async def is_available(self) -> bool:
        """Check if Ollama is available and running."""
        try:
            session = await self._get_session()
            url = urljoin(self.base_url, '/api/tags')
            
            async with session.get(url) as response:
                return response.status == 200
                
        except Exception:
            return False
    
    def get_provider_name(self) -> str:
        """Get the provider name."""
        return 'ollama'
    
    async def load_model(self, model: str) -> None:
        """Pre-load a model in Ollama."""
        try:
            session = await self._get_session()
            url = urljoin(self.base_url, '/api/generate')
            
            # Send a minimal request to load the model
            payload = {
                'model': model,
                'prompt': '',
                'stream': False,
                'options': {'num_predict': 1}
            }
            
            async with session.post(url, json=payload) as response:
                # We don't care about the response, just that the model loads
                pass
                
        except Exception as e:
            print(f"Error pre-loading model {model}: {e}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - close session."""
        if self._session and not self._session.closed:
            await self._session.close()