"""Optimized response handler for Think AI with O(1) performance."""

import random
from typing import Dict, List, Any, Optional
from datetime import datetime


class OptimizedResponder:
    """Direct, helpful response generation with O(1) lookup times."""
    
    def __init__(self):
        """Initialize with pre-computed response patterns."""
        # O(1) hash table for instant response lookup
        self.response_map = self._build_response_map()
        self.code_languages = {
            "python", "javascript", "js", "java", "c++", "cpp",
            "go", "rust", "ruby", "typescript", "ts", "c#", "csharp"
        }
        
    def _build_response_map(self) -> Dict[str, str]:
        """Build O(1) response lookup table."""
        return {
            # Direct greetings
            "hello": "Hello! I'm Think AI, ready to help you with any questions or tasks.",
            "hi": "Hi there! How can I assist you today?",
            "hey": "Hey! What can I help you with?",
            
            # Direct questions
            "what do u know": "I know programming, AI concepts, problem-solving, and can help with code generation, explanations, and technical discussions. Ask me anything!",
            "what do you know": "I have knowledge in software development, AI/ML, algorithms, data structures, and can generate code in multiple languages. What would you like to explore?",
            
            # Capabilities
            "can u code": "Yes! I can write code in Python, JavaScript, Java, C++, Go, Rust, and more. What would you like me to build?",
            "can you code": "Absolutely! I excel at coding in many languages. Tell me what you need - algorithms, web apps, scripts, or any other program.",
            
            # About me
            "who are you": "I'm Think AI - an intelligent assistant focused on helping you solve problems, write code, and learn new concepts efficiently.",
            "what are you": "I'm an AI assistant specialized in programming, problem-solving, and providing clear, direct answers to your questions.",
        }
    
    def get_response(self, query: str) -> str:
        """Get direct response with O(1) complexity."""
        query_lower = query.lower().strip()
        
        # Direct O(1) lookup
        if query_lower in self.response_map:
            return self.response_map[query_lower]
        
        # Handle pattern-based queries
        if self._is_greeting(query_lower):
            return "Hello! How can I help you today?"
            
        if self._is_code_request(query_lower):
            return self._handle_code_request(query_lower)
            
        if self._is_capability_question(query_lower):
            return self._handle_capability_question(query_lower)
            
        if self._is_knowledge_question(query_lower):
            return self._handle_knowledge_question(query_lower)
            
        # Default helpful response
        return self._generate_helpful_response(query)
    
    def _is_greeting(self, query: str) -> bool:
        """Check if query is a greeting - O(1)."""
        greetings = {"hello", "hi", "hey", "greetings", "hola"}
        return any(greet in query for greet in greetings)
    
    def _is_code_request(self, query: str) -> bool:
        """Check if query is about coding - O(1)."""
        code_keywords = {"code", "program", "script", "function", "class"}
        return any(keyword in query for keyword in code_keywords)
    
    def _is_capability_question(self, query: str) -> bool:
        """Check if asking about capabilities - O(1)."""
        capability_keywords = {"can you", "can u", "do you", "are you able"}
        return any(keyword in query for keyword in capability_keywords)
    
    def _is_knowledge_question(self, query: str) -> bool:
        """Check if asking about knowledge - O(1)."""
        knowledge_keywords = {"what do you know", "what do u know", "your knowledge"}
        return any(keyword in query for keyword in knowledge_keywords)
    
    def _handle_code_request(self, query: str) -> str:
        """Handle coding requests directly."""
        # Detect language
        for lang in self.code_languages:
            if lang in query:
                return f"I'll write {lang.upper()} code for you. What specific functionality do you need?"
        
        if "hello world" in query:
            return "I can write Hello World in any language! Which one: Python, JavaScript, Java, C++, Go, Rust, or another?"
        
        return "Yes, I can code! What would you like me to create? Specify the language and functionality."
    
    def _handle_capability_question(self, query: str) -> str:
        """Handle capability questions directly."""
        if "code" in query:
            return "Yes, I can write professional code in multiple languages with best practices and optimizations."
        
        return "I can help with programming, debugging, explanations, algorithms, and technical problem-solving."
    
    def _handle_knowledge_question(self, query: str) -> str:
        """Handle knowledge questions directly."""
        return """I have expertise in:
• Programming languages (Python, JS, Java, C++, Go, Rust)
• Algorithms and data structures
• Web development and APIs
• AI/ML concepts
• System design and architecture
• Debugging and optimization

What topic interests you?"""
    
    def _generate_helpful_response(self, query: str) -> str:
        """Generate helpful response for unmatched queries."""
        # Be direct and honest
        return f"I understand you're asking about '{query}'. Could you provide more details so I can give you a specific, helpful answer?"