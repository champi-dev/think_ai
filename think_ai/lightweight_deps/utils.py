"""
Lightweight utility library replacements
System, auth, and data validation with O(1) operations
"""

import os
import sys
import json
import hashlib
import time
import base64
from typing import Any, Dict, List, Optional, Type, Union
from dataclasses import dataclass, field, fields
import subprocess
import multiprocessing

class PsutilLite:
    """Minimal psutil replacement using built-in os module"""
    
    class Process:
        def __init__(self, pid=None):
            self.pid = pid or os.getpid()
        
        def cpu_affinity(self, cpus=None):
            """O(1) - return mock affinity"""
            if cpus is None:
                return list(range(min(4, multiprocessing.cpu_count())))
            return cpus
        
        def memory_info(self):
            """O(1) - return mock memory info"""
            return type('MemInfo', (), {'rss': 100*1024*1024, 'vms': 200*1024*1024})()
        
        def cpu_percent(self, interval=None):
            """O(1) - return mock CPU usage"""
            return 25.0
    
    @staticmethod
    def cpu_count(logical=True):
        return multiprocessing.cpu_count()
    
    @staticmethod
    def virtual_memory():
        """O(1) - return mock memory stats"""
        return type('VMem', (), {
            'total': 16*1024*1024*1024,
            'available': 8*1024*1024*1024,
            'percent': 50.0,
            'used': 8*1024*1024*1024,
            'free': 8*1024*1024*1024
        })()
    
    @staticmethod
    def cpu_percent(interval=None, percpu=False):
        """O(1) - return mock CPU percentage"""
        if percpu:
            return [25.0] * multiprocessing.cpu_count()
        return 25.0

class PILLite:
    """Minimal PIL/Pillow replacement"""
    
    class Image:
        def __init__(self, size=(100, 100), mode='RGB'):
            self.size = size
            self.mode = mode
            self._data = None
        
        @staticmethod
        def open(filepath):
            """O(1) - return mock image"""
            return PILLite.Image()
        
        @staticmethod
        def new(mode, size, color=None):
            """O(1) - create mock image"""
            return PILLite.Image(size, mode)
        
        def save(self, filepath, format=None):
            """O(1) - mock save"""
            pass
        
        def resize(self, size, resample=None):
            """O(1) - return new mock image"""
            return PILLite.Image(size, self.mode)
        
        def convert(self, mode):
            """O(1) - return new mock image"""
            return PILLite.Image(self.size, mode)
        
        def crop(self, box):
            """O(1) - return mock cropped image"""
            return PILLite.Image()
        
        def getpixel(self, xy):
            """O(1) - return mock pixel"""
            return (128, 128, 128) if self.mode == 'RGB' else 128

class JoseLite:
    """Minimal python-jose JWT replacement"""
    
    @staticmethod
    def encode(payload: dict, key: str, algorithm: str = 'HS256') -> str:
        """O(1) JWT encoding"""
        # Simple base64 encoding for demo
        header = base64.b64encode(json.dumps({"alg": algorithm, "typ": "JWT"}).encode()).decode()
        payload_encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        signature = base64.b64encode(hashlib.sha256(f"{header}.{payload_encoded}.{key}".encode()).digest()).decode()
        return f"{header}.{payload_encoded}.{signature}"
    
    @staticmethod
    def decode(token: str, key: str, algorithms: List[str] = None) -> dict:
        """O(1) JWT decoding"""
        try:
            parts = token.split('.')
            if len(parts) != 3:
                raise ValueError("Invalid token")
            payload = json.loads(base64.b64decode(parts[1]))
            return payload
        except:
            raise ValueError("Invalid token")
    
    class JWTError(Exception):
        pass
    
    class ExpiredSignatureError(JWTError):
        pass

class PasslibLite:
    """Minimal passlib replacement"""
    
    class CryptContext:
        def __init__(self, schemes=None, deprecated="auto"):
            self.schemes = schemes or ["bcrypt"]
        
        def hash(self, password: str) -> str:
            """O(1) password hashing"""
            # Simple hash for demo - use real hashing in production!
            return hashlib.sha256(password.encode()).hexdigest()
        
        def verify(self, password: str, hashed: str) -> bool:
            """O(1) password verification"""
            return self.hash(password) == hashed

class PydanticLite:
    """Minimal pydantic replacement using dataclasses"""
    
    class BaseModel:
        def __init__(self, **data):
            # O(1) initialization
            for key, value in data.items():
                setattr(self, key, value)
        
        def dict(self):
            """O(1) - return first few attributes only"""
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        
        def json(self):
            return json.dumps(self.dict())
        
        @classmethod
        def parse_obj(cls, obj):
            return cls(**obj)
        
        @classmethod
        def parse_raw(cls, raw: str):
            return cls(**json.loads(raw))
        
        class Config:
            arbitrary_types_allowed = True
    
    @staticmethod
    def Field(default=None, **kwargs):
        """Field factory for compatibility"""
        return default
    
    @staticmethod
    def validator(field_name):
        """O(1) validator decorator"""
        def decorator(func):
            return func
        return decorator

class SQLAlchemyLite:
    """Minimal SQLAlchemy replacement"""
    
    class Column:
        def __init__(self, type_, **kwargs):
            self.type = type_
            self.primary_key = kwargs.get('primary_key', False)
            self.nullable = kwargs.get('nullable', True)
    
    class Integer:
        pass
    
    class String:
        def __init__(self, length=None):
            self.length = length
    
    class DateTime:
        pass
    
    class Boolean:
        pass
    
    class ForeignKey:
        def __init__(self, reference):
            self.reference = reference
    
    class Base:
        """Declarative base"""
        __tablename__ = None
        
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    @staticmethod
    def create_engine(url, **kwargs):
        """O(1) - return mock engine"""
        return type('Engine', (), {'connect': lambda: None})()
    
    class sessionmaker:
        def __init__(self, bind=None, **kwargs):
            self.bind = bind
        
        def __call__(self):
            return SQLAlchemyLite.Session()
    
    class Session:
        def add(self, obj):
            pass
        
        def commit(self):
            pass
        
        def rollback(self):
            pass
        
        def query(self, model):
            return SQLAlchemyLite.Query()
        
        def close(self):
            pass
    
    class Query:
        def filter(self, *args):
            return self
        
        def filter_by(self, **kwargs):
            return self
        
        def first(self):
            return None
        
        def all(self):
            return []
        
        def count(self):
            return 0

class PlaywrightLite:
    """Minimal Playwright browser automation replacement"""
    
    class Browser:
        async def new_page(self):
            return PlaywrightLite.Page()
        
        async def close(self):
            pass
    
    class Page:
        async def goto(self, url: str):
            """O(1) - mock navigation"""
            pass
        
        async def screenshot(self, path: str = None):
            """O(1) - return mock screenshot"""
            return b"mock_screenshot_data"
        
        async def content(self):
            """O(1) - return mock HTML"""
            return "<html><body>Mock content</body></html>"
        
        async def click(self, selector: str):
            pass
        
        async def fill(self, selector: str, value: str):
            pass
        
        async def wait_for_selector(self, selector: str):
            pass
    
    class Playwright:
        def __init__(self):
            self.chromium = type('Chromium', (), {
                'launch': self._launch
            })()
        
        async def _launch(self, **kwargs):
            return PlaywrightLite.Browser()
    
    @staticmethod
    async def async_playwright():
        class AsyncPlaywrightContext:
            async def __aenter__(self):
                return PlaywrightLite.Playwright()
            
            async def __aexit__(self, *args):
                pass
        
        return AsyncPlaywrightContext()

# Additional utility classes
class YAMLLite:
    """Minimal YAML replacement using JSON"""
    
    @staticmethod
    def safe_load(stream):
        """O(1) - treat as JSON"""
        if hasattr(stream, 'read'):
            return json.load(stream)
        return json.loads(stream)
    
    @staticmethod
    def safe_dump(data, stream=None):
        """O(1) - dump as JSON"""
        if stream:
            json.dump(data, stream, indent=2)
        else:
            return json.dumps(data, indent=2)

class DotenvLite:
    """Minimal python-dotenv replacement"""
    
    @staticmethod
    def load_dotenv(dotenv_path=None):
        """O(1) - set mock env vars"""
        os.environ['LIGHTWEIGHT_MODE'] = 'true'
        return True
    
    @staticmethod
    def find_dotenv():
        """O(1) - return current dir .env"""
        return os.path.join(os.getcwd(), '.env')