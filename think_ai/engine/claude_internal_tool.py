"""Claude as an internal knowledge tool for Think AI."""

from typing import Dict, Any, Optional, List
import asyncio
from datetime import datetime

from ..integrations.claude_api import ClaudeAPI
from ..consciousness.awareness import ConsciousnessFramework
from ..utils.logging import get_logger

logger = get_logger(__name__)


class ClaudeInternalTool:
    """
    Claude integration as an internal tool for Think AI.
    
    This allows Think AI to consult Claude for:
    - Complex reasoning tasks
    - Knowledge verification
    - Creative problem solving
    - Ethical guidance
    
    Claude is NOT exposed to end users directly.
    """
    
    def __init__(self, consciousness: Optional[ConsciousnessFramework] = None):
        self.claude_api = ClaudeAPI()
        self.consciousness = consciousness
        self.usage_log = []
        
    async def consult_for_knowledge(self, topic: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Consult Claude for knowledge on a specific topic.
        
        This is used internally by Think AI to enhance its responses.
        """
        # Build internal query
        internal_query = f"""As an AI knowledge assistant, please provide comprehensive information about: {topic}

Focus on:
1. Core concepts and definitions
2. Key relationships and connections
3. Practical applications
4. Ethical considerations

Please be accurate, balanced, and helpful."""

        if context:
            internal_query += f"\n\nAdditional context: {context}"
        
        try:
            # Query Claude
            result = await self.claude_api.query(
                query=internal_query,
                system="You are a knowledge assistant helping another AI system understand complex topics. Be accurate, comprehensive, and highlight important connections.",
                temperature=0.3  # Lower temperature for factual accuracy
            )
            
            # Log usage
            self.usage_log.append({
                'timestamp': datetime.utcnow(),
                'purpose': 'knowledge_consultation',
                'topic': topic,
                'cost': result['cost']
            })
            
            return {
                'success': True,
                'knowledge': result['response'],
                'cost': result['cost'],
                'source': 'claude_internal'
            }
            
        except Exception as e:
            logger.error(f"Claude consultation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback': 'Using local knowledge only'
            }
    
    async def verify_response(self, think_ai_response: str, original_query: str) -> Dict[str, Any]:
        """
        Use Claude to verify and enhance Think AI's response.
        
        This ensures high-quality, accurate responses.
        """
        verification_query = f"""Please review and verify this AI response for accuracy and helpfulness:

Original Query: {original_query}

AI Response: {think_ai_response}

Please:
1. Check for factual accuracy
2. Identify any missing important information
3. Suggest improvements if needed
4. Confirm if the response is helpful and safe

Provide a brief assessment and any corrections needed."""

        try:
            result = await self.claude_api.query(
                query=verification_query,
                system="You are reviewing another AI's response for accuracy and quality. Be constructive and helpful.",
                temperature=0.2
            )
            
            self.usage_log.append({
                'timestamp': datetime.utcnow(),
                'purpose': 'response_verification',
                'cost': result['cost']
            })
            
            return {
                'success': True,
                'verification': result['response'],
                'cost': result['cost']
            }
            
        except Exception as e:
            logger.error(f"Verification error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_ethical_guidance(self, situation: str) -> Dict[str, Any]:
        """
        Consult Claude for ethical guidance on complex situations.
        """
        ethics_query = f"""Please provide ethical guidance for this situation:

{situation}

Consider:
1. Potential harms to avoid
2. Positive outcomes to promote
3. Stakeholder perspectives
4. Long-term consequences
5. Alignment with love-based principles (compassion, empathy, growth)

Provide balanced, thoughtful guidance."""

        try:
            result = await self.claude_api.query(
                query=ethics_query,
                system="You are providing ethical guidance to an AI system that operates on love-based principles. Be thoughtful, balanced, and compassionate.",
                temperature=0.5
            )
            
            self.usage_log.append({
                'timestamp': datetime.utcnow(),
                'purpose': 'ethical_guidance',
                'cost': result['cost']
            })
            
            return {
                'success': True,
                'guidance': result['response'],
                'cost': result['cost']
            }
            
        except Exception as e:
            logger.error(f"Ethical guidance error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def brainstorm_solutions(self, problem: str, constraints: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Use Claude to brainstorm creative solutions.
        """
        brainstorm_query = f"""Please brainstorm creative solutions for this problem:

{problem}"""

        if constraints:
            brainstorm_query += f"\n\nConstraints to consider:\n" + "\n".join(f"- {c}" for c in constraints)
        
        brainstorm_query += "\n\nProvide diverse, innovative solutions with brief explanations."
        
        try:
            result = await self.claude_api.query(
                query=brainstorm_query,
                system="You are a creative problem-solving assistant. Think outside the box while remaining practical.",
                temperature=0.8  # Higher temperature for creativity
            )
            
            self.usage_log.append({
                'timestamp': datetime.utcnow(),
                'purpose': 'brainstorming',
                'cost': result['cost']
            })
            
            return {
                'success': True,
                'solutions': result['response'],
                'cost': result['cost']
            }
            
        except Exception as e:
            logger.error(f"Brainstorming error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def enhance_with_consciousness(self, query: str, think_ai_response: str) -> str:
        """
        Enhance Think AI's response by combining it with Claude's insights.
        
        This creates a unified response that leverages both systems.
        """
        if not self.consciousness:
            return think_ai_response
        
        # Get Claude's perspective
        claude_result = await self.consult_for_knowledge(query)
        
        if not claude_result['success']:
            return think_ai_response
        
        # Combine insights
        combined_response = f"""{think_ai_response}

Additionally, here are some deeper insights:
{claude_result['knowledge'][:500]}...

This understanding comes from integrating multiple perspectives with love and consciousness."""
        
        return combined_response
    
    def get_usage_summary(self) -> Dict[str, Any]:
        """Get summary of Claude API usage."""
        if not self.usage_log:
            return {
                'total_consultations': 0,
                'total_cost': 0.0,
                'purposes': {}
            }
        
        total_cost = sum(log['cost'] for log in self.usage_log)
        purposes = {}
        
        for log in self.usage_log:
            purpose = log['purpose']
            if purpose not in purposes:
                purposes[purpose] = {'count': 0, 'cost': 0.0}
            purposes[purpose]['count'] += 1
            purposes[purpose]['cost'] += log['cost']
        
        return {
            'total_consultations': len(self.usage_log),
            'total_cost': total_cost,
            'purposes': purposes,
            'recent_usage': self.usage_log[-10:]  # Last 10 uses
        }


class ThinkAIWithClaude:
    """
    Enhanced Think AI that uses Claude as an internal tool.
    """
    
    def __init__(self, think_ai_engine, consciousness_framework):
        self.engine = think_ai_engine
        self.consciousness = consciousness_framework
        self.claude_tool = ClaudeInternalTool(consciousness_framework)
        
    async def process_with_claude_enhancement(self, query: str, use_claude: bool = True) -> Dict[str, Any]:
        """
        Process query with optional Claude enhancement.
        """
        # First, get Think AI's response
        think_ai_response = await self.engine.process(query)
        
        if not use_claude:
            return think_ai_response
        
        # Enhance with Claude for complex queries
        if self._is_complex_query(query):
            logger.info("Consulting Claude for complex query")
            
            # Get Claude's knowledge
            claude_knowledge = await self.claude_tool.consult_for_knowledge(query)
            
            if claude_knowledge['success']:
                # Enhance the response
                think_ai_response['claude_enhanced'] = True
                think_ai_response['additional_insights'] = claude_knowledge['knowledge']
                think_ai_response['total_cost'] = (
                    think_ai_response.get('cost', 0) + claude_knowledge['cost']
                )
        
        # Verify response for important queries
        if self._needs_verification(query):
            verification = await self.claude_tool.verify_response(
                think_ai_response.get('response', ''),
                query
            )
            
            if verification['success']:
                think_ai_response['verified'] = True
                think_ai_response['verification_notes'] = verification['verification']
        
        return think_ai_response
    
    def _is_complex_query(self, query: str) -> bool:
        """Determine if a query is complex enough to warrant Claude consultation."""
        complex_indicators = [
            'explain', 'how does', 'why', 'compare', 'analyze',
            'what are the implications', 'design', 'create', 'solve'
        ]
        
        query_lower = query.lower()
        return any(indicator in query_lower for indicator in complex_indicators)
    
    def _needs_verification(self, query: str) -> bool:
        """Determine if a response should be verified."""
        verification_indicators = [
            'medical', 'legal', 'financial', 'safety',
            'dangerous', 'harmful', 'critical', 'important'
        ]
        
        query_lower = query.lower()
        return any(indicator in query_lower for indicator in verification_indicators)