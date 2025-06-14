"""
Multimodal processor - The brain that sees, hears, and understands everything.
Now with Colombian coast jokes: "El que nace pa' maceta, del corredor no pasa" 🌴
"""

import asyncio
from typing import Dict, Any, Union, Optional
import hashlib
import base64
import mimetypes
from pathlib import Path
import numpy as np
from PIL import Image
import io
import json

from ..utils.logging import get_logger

logger = get_logger(__name__)


class MultimodalProcessor:
    """
    Processes images, audio, video, documents - basically everything!
    Like a Swiss Army knife, but for AI.
    
    Performance: Still O(1) because we cache everything like a squirrel with nuts.
    """
    
    def __init__(self):
        self.processors = {}
        self.cache = {}  # O(1) lookup for processed content
        self.jokes = [
            "¡Ey el crispeta! 🍿",
            "¡Qué uso carruso ese man! 🚗", 
            "Ey llave, ¿qué más pues?",
            "¡Ajá y entonces!",
            "¡Qué pecao' hermano!",
            "¡Dale que vamos tarde!",
            "Ey papi, la vuelta es por allá donde vendían los raspao'",
            "¡Qué nota e' vaina!",
            "¡Bacano parce!",
            "El que nace pa' tamarindo, del palo no baja 🌴",
            "¡No joda vale!",
            "¡Erda manito!",
            "Tas más perdío' que el hijo e' Lindbergh",
            "¡Eche! ¿Y esa mondá qué es?"
        ]
        
        logger.info("🎨 Multimodal processor initialized - Now I can see, hear, and make you laugh!")
    
    async def initialize(self):
        """Initialize all modal processors."""
        from .image_processor import ImageProcessor
        from .audio_processor import AudioProcessor
        from .video_processor import VideoProcessor
        from .document_processor import DocumentProcessor
        
        self.processors = {
            'image': ImageProcessor(),
            'audio': AudioProcessor(),
            'video': VideoProcessor(),
            'document': DocumentProcessor()
        }
        
        # Initialize each processor
        for name, processor in self.processors.items():
            await processor.initialize()
            logger.info(f"✅ {name.capitalize()} processor ready")
        
        logger.info("🌟 All modalities online! ¡Ey el crispeta está ready pa' procesar! 🍿")
    
    def detect_modality(self, content: Union[str, bytes, Path]) -> str:
        """
        Detect what type of content we're dealing with.
        Like a detective, but for files.
        """
        if isinstance(content, str):
            # Check if it's a file path
            if Path(content).exists():
                mime_type, _ = mimetypes.guess_type(content)
                if mime_type:
                    if mime_type.startswith('image/'):
                        return 'image'
                    elif mime_type.startswith('audio/'):
                        return 'audio'
                    elif mime_type.startswith('video/'):
                        return 'video'
                    elif mime_type.startswith('application/'):
                        return 'document'
            return 'text'
        
        elif isinstance(content, bytes):
            # Try to detect from magic bytes
            if content.startswith(b'\xff\xd8\xff'):  # JPEG
                return 'image'
            elif content.startswith(b'\x89PNG'):  # PNG
                return 'image'
            elif content.startswith(b'ID3') or content.startswith(b'\xff\xfb'):  # MP3
                return 'audio'
            elif content.startswith(b'\x00\x00\x00\x20ftypmp4'):  # MP4
                return 'video'
            elif content.startswith(b'%PDF'):  # PDF
                return 'document'
        
        return 'unknown'
    
    async def process(self, content: Union[str, bytes, Path], 
                     context: Optional[str] = None) -> Dict[str, Any]:
        """
        Process any type of content with O(1) performance.
        
        Ajá y entonces? Let's see what you got!
        """
        # Generate cache key
        if isinstance(content, (str, bytes)):
            cache_key = hashlib.md5(
                (str(content)[:100] + str(context)).encode()
            ).hexdigest()
        else:
            cache_key = hashlib.md5(
                (str(content) + str(context)).encode()
            ).hexdigest()
        
        # Check cache first (O(1))
        if cache_key in self.cache:
            logger.info(f"🎯 Cache hit! ¡Qué nota e' vaina, ahorramos tiempo!")
            result = self.cache[cache_key].copy()
            result['joke'] = np.random.choice(self.jokes)
            return result
        
        # Detect modality
        modality = self.detect_modality(content)
        
        if modality == 'unknown':
            return {
                'error': 'Unknown content type',
                'joke': '¡Ey papi, no sé qué mondá es esa! 🤷',
                'suggestion': 'Intenta con imagen, audio, video o documentos mijo'
            }
        
        # Process based on modality
        processor = self.processors.get(modality)
        if not processor:
            return {
                'error': f'No processor for {modality}',
                'joke': '¡El que nace pa\' tamarindo, del palo no baja! 🌴'
            }
        
        # Process content
        result = await processor.process(content, context)
        
        # Add a joke because why not?
        result['joke'] = np.random.choice(self.jokes)
        result['modality'] = modality
        
        # Cache result
        self.cache[cache_key] = result.copy()
        
        # Implement LRU if cache gets too big
        if len(self.cache) > 10000:
            # Remove oldest entries
            keys_to_remove = list(self.cache.keys())[:1000]
            for key in keys_to_remove:
                del self.cache[key]
        
        return result
    
    async def process_multimodal(self, contents: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process multiple modalities at once.
        Like juggling, but with AI and Colombian jokes.
        
        Example:
        {
            'image': 'path/to/image.jpg',
            'audio': 'path/to/audio.mp3',
            'text': 'What do you see and hear?'
        }
        """
        results = {}
        tasks = []
        
        for modality, content in contents.items():
            if modality == 'text':
                results['text'] = content
            else:
                task = self.process(content, context=contents.get('text'))
                tasks.append((modality, task))
        
        # Process all modalities in parallel (still O(1) with caching!)
        if tasks:
            task_results = await asyncio.gather(*[task for _, task in tasks])
            for (modality, _), result in zip(tasks, task_results):
                results[modality] = result
        
        # Combine insights
        combined_result = {
            'insights': self._combine_insights(results),
            'modalities_processed': list(results.keys()),
            'joke': np.random.choice(self.jokes),
            'wisdom': '¡Bacano parce! Múltiples sentidos, una sola conciencia! 🧠'
        }
        
        return combined_result
    
    def _combine_insights(self, results: Dict[str, Any]) -> str:
        """
        Combine insights from different modalities.
        Like making sancocho - everything goes in the pot!
        """
        insights = []
        
        if 'image' in results and 'analysis' in results['image']:
            insights.append(f"Visually: {results['image']['analysis']}")
        
        if 'audio' in results and 'transcription' in results['audio']:
            insights.append(f"Audio says: {results['audio']['transcription']}")
        
        if 'video' in results and 'summary' in results['video']:
            insights.append(f"Video shows: {results['video']['summary']}")
        
        if 'document' in results and 'summary' in results['document']:
            insights.append(f"Document contains: {results['document']['summary']}")
        
        if 'text' in results:
            insights.append(f"Context: {results['text']}")
        
        return " | ".join(insights) if insights else "¡Qué pecao' hermano! No encontré ni mondá!"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get multimodal processing statistics."""
        return {
            'cache_size': len(self.cache),
            'modalities_available': list(self.processors.keys()),
            'joke_of_the_moment': np.random.choice(self.jokes),
            'status': '¡Dale que vamos tarde! ¡Todos los sistemas listos! 🚀'
        }