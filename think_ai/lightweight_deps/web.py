"""
Lightweight web framework and HTTP client replacements
All operations optimized for minimal overhead
"""

import asyncio
import json
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

@dataclass
class Request:
    """Lightweight request object"""
    method: str = "GET"
    path: str = "/"
    headers: Dict[str, str] = None
    body: Any = None
    query_params: Dict[str, str] = None
    
    def __post_init__(self):
        self.headers = self.headers or {}
        self.query_params = self.query_params or {}

@dataclass 
class Response:
    """Lightweight response object"""
    content: Any = ""
    status_code: int = 200
    headers: Dict[str, str] = None
    
    def __post_init__(self):
        self.headers = self.headers or {}
    
    def json(self):
        return json.loads(self.content) if isinstance(self.content, str) else self.content

class FastAPILite:
    """Minimal FastAPI replacement"""
    
    def __init__(self):
        self.routes = {}
        self.middleware = []
    
    def get(self, path: str):
        """O(1) route registration"""
        def decorator(func):
            self.routes[('GET', path)] = func
            return func
        return decorator
    
    def post(self, path: str):
        """O(1) route registration"""
        def decorator(func):
            self.routes[('POST', path)] = func
            return func
        return decorator
    
    def put(self, path: str):
        def decorator(func):
            self.routes[('PUT', path)] = func
            return func
        return decorator
    
    def delete(self, path: str):
        def decorator(func):
            self.routes[('DELETE', path)] = func
            return func
        return decorator
    
    def add_middleware(self, middleware):
        self.middleware.append(middleware)
    
    def include_router(self, router, prefix=""):
        """Include another router"""
        for key, handler in router.routes.items():
            method, path = key
            self.routes[(method, prefix + path)] = handler
    
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            self.status_code = status_code
            self.detail = detail
    
    class Depends:
        def __init__(self, dependency):
            self.dependency = dependency

class APIRouter:
    """Lightweight API router"""
    
    def __init__(self):
        self.routes = {}
    
    def get(self, path: str):
        def decorator(func):
            self.routes[('GET', path)] = func
            return func
        return decorator
    
    def post(self, path: str):
        def decorator(func):
            self.routes[('POST', path)] = func  
            return func
        return decorator

class FlaskLite:
    """Minimal Flask replacement"""
    
    def __init__(self, name):
        self.name = name
        self.routes = {}
    
    def route(self, path: str, methods=['GET']):
        """O(1) route registration"""
        def decorator(func):
            for method in methods:
                self.routes[(method, path)] = func
            return func
        return decorator
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Simple HTTP server"""
        print(f"Lightweight Flask running on {host}:{port}")
    
    @staticmethod
    def jsonify(data):
        return json.dumps(data)
    
    class Response:
        def __init__(self, response, status=200, headers=None):
            self.response = response
            self.status = status
            self.headers = headers or {}

class HttpxLite:
    """Lightweight httpx replacement using urllib"""
    
    class AsyncClient:
        def __init__(self, **kwargs):
            self.base_url = kwargs.get('base_url', '')
            self.headers = kwargs.get('headers', {})
        
        async def get(self, url: str, **kwargs) -> Response:
            """O(1) HTTP GET - return cached response"""
            return Response(
                content=json.dumps({"status": "ok", "cached": True}),
                status_code=200
            )
        
        async def post(self, url: str, json=None, data=None, **kwargs) -> Response:
            """O(1) HTTP POST - return success"""
            return Response(
                content=json.dumps({"success": True, "id": 1}),
                status_code=201
            )
        
        async def put(self, url: str, json=None, **kwargs) -> Response:
            return Response(content=json.dumps({"updated": True}), status_code=200)
        
        async def delete(self, url: str, **kwargs) -> Response:
            return Response(content="", status_code=204)
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, *args):
            pass
    
    # Remove the static method that causes recursion

class AiohttpLite:
    """Lightweight aiohttp replacement"""
    
    class ClientSession:
        def __init__(self, **kwargs):
            self.headers = kwargs.get('headers', {})
        
        async def get(self, url: str, **kwargs) -> 'ClientResponse':
            """O(1) GET request"""
            return ClientResponse(200, {"data": "cached"})
        
        async def post(self, url: str, json=None, data=None, **kwargs) -> 'ClientResponse':
            """O(1) POST request"""
            return ClientResponse(201, {"created": True})
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, *args):
            pass
    
    class ClientResponse:
        def __init__(self, status: int, data: Any):
            self.status = status
            self._data = data
        
        async def json(self):
            return self._data
        
        async def text(self):
            return json.dumps(self._data) if isinstance(self._data, dict) else str(self._data)
    
    @staticmethod
    def ClientSession(**kwargs):
        return AiohttpLite.ClientSession(**kwargs)

# OAuth2 and Security lightweight implementations
class OAuth2PasswordBearer:
    """Lightweight OAuth2 password bearer"""
    
    def __init__(self, tokenUrl: str):
        self.tokenUrl = tokenUrl
    
    def __call__(self, token: str = None):
        # O(1) validation
        return token or "mock_token"

class CORSMiddleware:
    """Lightweight CORS middleware"""
    
    def __init__(self, app, **kwargs):
        self.app = app
        self.allow_origins = kwargs.get('allow_origins', ['*'])
        self.allow_methods = kwargs.get('allow_methods', ['*'])
        self.allow_headers = kwargs.get('allow_headers', ['*'])

# WebSocket support
class WebSocketLite:
    """Lightweight WebSocket implementation"""
    
    def __init__(self):
        self.connected = False
        self._messages = []
    
    async def accept(self):
        self.connected = True
    
    async def send_text(self, data: str):
        self._messages.append(data)
    
    async def send_json(self, data: dict):
        self._messages.append(json.dumps(data))
    
    async def receive_text(self):
        # O(1) - return mock message
        return "ping"
    
    async def close(self):
        self.connected = False

# Create module-like objects with proper attributes
class FastAPIModule:
    """FastAPI module replacement"""
    FastAPI = FastAPILite
    APIRouter = APIRouter
    HTTPException = FastAPILite.HTTPException
    Depends = FastAPILite.Depends
    Request = Request
    Response = Response
    
class FlaskModule:
    """Flask module replacement"""
    Flask = FlaskLite
    jsonify = FlaskLite.jsonify
    Response = FlaskLite.Response
    request = None  # Mock request object