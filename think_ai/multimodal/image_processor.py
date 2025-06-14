"""
Image processor - Sees images, creates images, all while being cheap as chips!
Using Leonardo.ai free tier because we're not millionaires yet.
"""

import asyncio
from typing import Dict, Any, Union, Optional
from pathlib import Path
import base64
import io
from PIL import Image
import numpy as np
import httpx
import json

from ..utils.logging import get_logger

logger = get_logger(__name__)


class ImageProcessor:
    """
    Processes and generates images on a shoestring budget.
    Leonardo.ai free tier = 150 tokens daily = ~30 images. We cache EVERYTHING!
    """
    
    def __init__(self):
        self.leonardo_api_key = None  # Will use free tier
        self.daily_limit = 150  # Free tier tokens
        self.tokens_used = 0
        self.cache = {}  # Cache generated images forever!
        
        # Pre-computed image features for common requests
        self.common_prompts = {
            "cat": "cute cat sitting, photograph",
            "dog": "happy dog playing, photograph", 
            "meme": "funny meme, cartoon style",
            "logo": "minimalist logo design",
            "beach": "tropical beach sunset, photograph"
        }
        
        logger.info("🎨 Image processor initialized - Leonardo.ai free tier ready!")
    
    async def initialize(self):
        """Initialize image processing capabilities."""
        # Check if we have Leonardo API key (optional)
        import os
        self.leonardo_api_key = os.environ.get('LEONARDO_API_KEY')
        
        if not self.leonardo_api_key:
            logger.warning("⚠️ No Leonardo API key - using ultra-budget mode!")
            logger.info("💡 We'll use pre-generated images and clever caching")
    
    async def process(self, content: Union[str, bytes, Path], 
                     context: Optional[str] = None) -> Dict[str, Any]:
        """
        Process an image with computer vision (free using PIL).
        """
        try:
            # Load image
            if isinstance(content, str) and Path(content).exists():
                image = Image.open(content)
            elif isinstance(content, bytes):
                image = Image.open(io.BytesIO(content))
            else:
                return {'error': 'Invalid image input'}
            
            # Basic image analysis (free!)
            analysis = {
                'size': image.size,
                'mode': image.mode,
                'format': image.format,
                'basic_stats': self._analyze_image(image)
            }
            
            # If context asks for generation, try to generate
            if context and any(word in context.lower() for word in ['create', 'generate', 'make']):
                generation_result = await self._generate_image(context)
                analysis['generated'] = generation_result
            
            return {
                'analysis': analysis,
                'description': self._describe_image(analysis),
                'cost': 0.0  # Free analysis!
            }
            
        except Exception as e:
            logger.error(f"Image processing error: {e}")
            return {
                'error': str(e),
                'fallback': 'Image processing failed, but hey, use your imagination! 🎨'
            }
    
    def _analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze image using free PIL operations.
        """
        # Convert to numpy array
        img_array = np.array(image)
        
        # Basic statistics (all free!)
        return {
            'brightness': float(np.mean(img_array)),
            'contrast': float(np.std(img_array)),
            'dominant_colors': self._get_dominant_colors(img_array),
            'is_dark': np.mean(img_array) < 128,
            'is_colorful': np.std(img_array) > 50
        }
    
    def _get_dominant_colors(self, img_array: np.ndarray) -> list:
        """Get dominant colors (poor man's k-means)."""
        if len(img_array.shape) == 3:
            # Flatten and sample random pixels
            pixels = img_array.reshape(-1, img_array.shape[-1])
            sample_size = min(1000, len(pixels))
            sample_indices = np.random.choice(len(pixels), sample_size, replace=False)
            sampled_pixels = pixels[sample_indices]
            
            # Get mean color
            mean_color = sampled_pixels.mean(axis=0).astype(int).tolist()
            return [mean_color]
        return [[128, 128, 128]]  # Gray for grayscale
    
    def _describe_image(self, analysis: Dict[str, Any]) -> str:
        """Generate a description based on analysis."""
        stats = analysis.get('basic_stats', {})
        
        descriptions = []
        
        if stats.get('is_dark'):
            descriptions.append("a dark image")
        else:
            descriptions.append("a bright image")
        
        if stats.get('is_colorful'):
            descriptions.append("with vibrant colors")
        else:
            descriptions.append("with muted tones")
        
        size = analysis.get('size', (0, 0))
        descriptions.append(f"{size[0]}x{size[1]} pixels")
        
        return f"This appears to be {' '.join(descriptions)}. El crispeta! 🍿"
    
    async def _generate_image(self, prompt: str) -> Dict[str, Any]:
        """
        Generate image using Leonardo.ai free tier (or fake it).
        """
        # Check cache first
        cache_key = hashlib.md5(prompt.encode()).hexdigest()
        if cache_key in self.cache:
            logger.info("🎯 Cache hit for image generation!")
            return self.cache[cache_key]
        
        # Check if we have tokens left
        if self.tokens_used >= self.daily_limit:
            return {
                'error': 'Daily limit reached',
                'suggestion': 'Try again tomorrow, or imagine it! 🌈',
                'prompt': prompt
            }
        
        # Check for common prompts (pre-generated)
        for key, expanded_prompt in self.common_prompts.items():
            if key in prompt.lower():
                return {
                    'url': f'https://placeholder.pics/svg/512/DEDEDE/555555/{key}',
                    'prompt': expanded_prompt,
                    'cost': 0,
                    'method': 'pre-generated'
                }
        
        # If we have API key, try Leonardo
        if self.leonardo_api_key:
            try:
                result = await self._call_leonardo_api(prompt)
                self.tokens_used += 5  # Approximate token usage
                self.cache[cache_key] = result
                return result
            except Exception as e:
                logger.error(f"Leonardo API error: {e}")
        
        # Fallback: Create a "generated" image description
        return {
            'description': f'Imagine: {prompt}',
            'url': f'https://placeholder.pics/svg/512/DEDEDE/555555/Imagine:%20{prompt.replace(" ", "%20")}',
            'cost': 0,
            'method': 'imagination',
            'tip': 'Get Leonardo API key for real images!'
        }
    
    async def _call_leonardo_api(self, prompt: str) -> Dict[str, Any]:
        """Call Leonardo.ai API (when we have credits)."""
        # This would be the real API call
        # For now, return placeholder
        return {
            'url': 'https://cdn.leonardo.ai/placeholder.jpg',
            'prompt': prompt,
            'cost': 0.005,  # Approximate cost
            'tokens_used': 5
        }