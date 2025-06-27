"""
Think AI - Core Types and Data Models
"""

from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field
from enum import Enum


class LogLevel(str, Enum):
    """Log levels for Think AI operations"""
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


class ThinkAIConfig(BaseModel):
    """Configuration for Think AI client"""
    base_url: str = Field(default="https://thinkai-production.up.railway.app", description="Base URL for Think AI API")
    timeout: int = Field(default=30, description="API timeout in seconds")
    debug: bool = Field(default=False, description="Enable debug logging")


class ChatRequest(BaseModel):
    """Request for chat/conversation with Think AI"""
    query: str = Field(description="User query/message")
    context: Optional[List[str]] = Field(default=None, description="Optional context for the conversation")
    max_length: Optional[int] = Field(default=None, description="Maximum response length")


class ChatResponse(BaseModel):
    """Response from Think AI chat"""
    response: str = Field(description="AI response text")
    context: Optional[List[str]] = Field(default=None, description="Context used for generating response")
    response_time_ms: int = Field(description="Response generation time in milliseconds")
    confidence: Optional[float] = Field(default=None, description="Confidence score (0-1)")


class HealthComponent(BaseModel):
    """Health status of individual system components"""
    knowledge_engine: bool = Field(description="Knowledge engine status")
    vector_search: bool = Field(description="Vector search status")
    ai_models: bool = Field(description="AI models status")
    database: bool = Field(description="Database status")


class HealthStatus(BaseModel):
    """System health status"""
    status: str = Field(description="Overall system status", pattern="^(healthy|degraded|unhealthy)$")
    details: Optional[HealthComponent] = Field(default=None, description="Detailed health information")
    timestamp: str = Field(description="Last health check timestamp")


class SystemStats(BaseModel):
    """System statistics and metrics"""
    total_nodes: int = Field(description="Total knowledge nodes in the system")
    training_iterations: int = Field(description="Number of training iterations completed")
    total_knowledge_items: int = Field(description="Total knowledge items processed")
    domain_distribution: Dict[str, int] = Field(description="Distribution of knowledge across domains")
    average_confidence: float = Field(description="Average confidence across all knowledge")
    uptime: Optional[int] = Field(default=None, description="System uptime in seconds")


class KnowledgeDomain(BaseModel):
    """Knowledge domain information"""
    name: str = Field(description="Domain name")
    count: int = Field(description="Number of knowledge items in this domain")
    activity: float = Field(description="Recent activity score")


class SearchResult(BaseModel):
    """Search result from knowledge base"""
    content: str = Field(description="Matching content")
    score: float = Field(description="Relevance score")
    domain: str = Field(description="Knowledge domain")
    related_concepts: List[str] = Field(description="Related concepts")


class StreamResponse(BaseModel):
    """Streaming response chunk"""
    chunk: str = Field(description="Response chunk")
    done: bool = Field(description="Whether this is the final chunk")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata for the chunk")


class ThinkAIError(Exception):
    """Custom exception for Think AI operations"""
    
    def __init__(
        self, 
        message: str, 
        status: Optional[int] = None, 
        code: Optional[str] = None, 
        details: Optional[Any] = None
    ):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.details = details
        
    def __str__(self) -> str:
        return f"ThinkAIError: {self.message}"
        
    def __repr__(self) -> str:
        return f"ThinkAIError(message='{self.message}', status={self.status}, code='{self.code}')"