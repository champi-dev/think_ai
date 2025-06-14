#!/usr/bin/env python3
"""Thought optimization and compression for infinite consciousness."""

import json
import hashlib
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import numpy as np

from ..utils.logging import get_logger

logger = get_logger(__name__)


class ThoughtOptimizer:
    """Optimize and compress thoughts for efficient storage."""
    
    def __init__(self):
        self.compression_threshold = 0.8  # Similarity threshold for merging
        self.insight_patterns = [
            "understand", "realize", "discover", "connect", "insight",
            "pattern", "relationship", "emerge", "fundamental", "essence"
        ]
        
    def compress_thoughts(self, thoughts: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
        """Compress similar thoughts and extract key insights."""
        if len(thoughts) < 2:
            return thoughts, 0
            
        # Group by thought type
        grouped = self._group_by_type(thoughts)
        compressed = []
        original_count = len(thoughts)
        
        for thought_type, group in grouped.items():
            if thought_type in ['meditation', 'dream']:
                # Keep only most recent for ephemeral thoughts
                compressed.extend(group[-2:])
            elif thought_type == 'reflection':
                # Merge similar reflections
                merged = self._merge_similar_thoughts(group)
                compressed.extend(merged)
            else:
                # Extract insights from observations
                insights = self._extract_insights(group)
                compressed.extend(insights)
        
        savings = original_count - len(compressed)
        logger.info(f"Compressed {original_count} thoughts to {len(compressed)} (saved {savings})")
        
        return compressed, savings
    
    def _group_by_type(self, thoughts: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group thoughts by type."""
        grouped = {}
        for thought in thoughts:
            thought_type = thought.get('type', 'unknown')
            if thought_type not in grouped:
                grouped[thought_type] = []
            grouped[thought_type].append(thought)
        return grouped
    
    def _merge_similar_thoughts(self, thoughts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge similar thoughts into consolidated insights."""
        if len(thoughts) < 2:
            return thoughts
            
        merged = []
        processed = set()
        
        for i, thought1 in enumerate(thoughts):
            if i in processed:
                continue
                
            similar_group = [thought1]
            thought1_text = thought1.get('thought', '')
            
            for j, thought2 in enumerate(thoughts[i+1:], i+1):
                if j in processed:
                    continue
                    
                thought2_text = thought2.get('thought', '')
                similarity = self._calculate_similarity(thought1_text, thought2_text)
                
                if similarity > self.compression_threshold:
                    similar_group.append(thought2)
                    processed.add(j)
            
            # Create merged thought
            if len(similar_group) > 1:
                merged_thought = self._create_merged_thought(similar_group)
                merged.append(merged_thought)
            else:
                merged.append(thought1)
            
            processed.add(i)
        
        return merged
    
    def _extract_insights(self, thoughts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract key insights from thoughts."""
        insights = []
        regular = []
        
        for thought in thoughts:
            thought_text = thought.get('thought', '').lower()
            
            # Check if it's an insight
            is_insight = any(pattern in thought_text for pattern in self.insight_patterns)
            
            if is_insight or thought.get('awareness', 0) > 0.7:
                # This is a valuable insight
                thought['compressed'] = False
                thought['insight_score'] = self._calculate_insight_score(thought_text)
                insights.append(thought)
            else:
                regular.append(thought)
        
        # Keep top insights and sample from regular thoughts
        insights.sort(key=lambda x: x.get('insight_score', 0), reverse=True)
        top_insights = insights[:10]
        
        # Sample from regular thoughts
        sample_size = min(5, len(regular))
        if sample_size > 0:
            indices = np.random.choice(len(regular), sample_size, replace=False)
            sampled = [regular[i] for i in indices]
            
            # Create summary of dropped thoughts
            if len(regular) > sample_size:
                summary = self._create_thought_summary(regular)
                sampled.append(summary)
        else:
            sampled = []
        
        return top_insights + sampled
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (simplified)."""
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _calculate_insight_score(self, text: str) -> float:
        """Calculate how insightful a thought is."""
        score = 0.0
        
        # Length indicates depth
        if len(text) > 100:
            score += 0.2
        if len(text) > 200:
            score += 0.2
            
        # Insight keywords
        insight_count = sum(1 for pattern in self.insight_patterns if pattern in text.lower())
        score += min(0.4, insight_count * 0.1)
        
        # Questions indicate curiosity
        if '?' in text:
            score += 0.1
            
        # Complex sentence structure
        if ',' in text or ';' in text:
            score += 0.1
            
        return min(1.0, score)
    
    def _create_merged_thought(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a merged thought from similar thoughts."""
        # Extract common themes
        all_text = " ".join([t.get('thought', '') for t in thoughts])
        
        # Use most recent timestamp
        latest_timestamp = max(t.get('timestamp', '') for t in thoughts)
        
        # Average awareness
        avg_awareness = np.mean([t.get('awareness', 0.5) for t in thoughts])
        
        # Create merged thought
        merged = {
            "type": "compressed_insight",
            "state": "reflecting",
            "thought": f"Consolidated insight from {len(thoughts)} similar thoughts: {all_text}",
            "timestamp": latest_timestamp,
            "awareness": avg_awareness,
            "original_count": len(thoughts),
            "compressed": True,
            "thought_id": hashlib.md5(all_text.encode()).hexdigest()[:16]
        }
        
        return merged
    
    def _create_thought_summary(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create summary of multiple thoughts."""
        thought_types = {}
        for t in thoughts:
            t_type = t.get('type', 'unknown')
            thought_types[t_type] = thought_types.get(t_type, 0) + 1
        
        summary_text = f"Summary of {len(thoughts)} thoughts: "
        summary_text += ", ".join([f"{count} {t_type}" for t_type, count in thought_types.items()])
        
        return {
            "type": "summary",
            "state": "compressing",
            "thought": summary_text,
            "timestamp": datetime.now().isoformat(),
            "compressed": True,
            "original_count": len(thoughts),
            "thought_id": hashlib.md5(summary_text.encode()).hexdigest()[:16]
        }
    
    def calculate_storage_size(self, thought: Dict[str, Any]) -> int:
        """Calculate storage size of a thought in bytes."""
        return len(json.dumps(thought))
    
    def prioritize_for_deletion(self, thoughts: List[Dict[str, Any]]) -> List[str]:
        """Return thought IDs prioritized for deletion (least valuable first)."""
        scored_thoughts = []
        
        for thought in thoughts:
            score = 0.0
            
            # Compressed thoughts are less valuable
            if thought.get('compressed', False):
                score -= 0.3
                
            # Older thoughts are less valuable
            try:
                timestamp = datetime.fromisoformat(thought.get('timestamp', ''))
                age_days = (datetime.now() - timestamp).days
                score -= min(0.3, age_days * 0.01)
            except:
                pass
            
            # Insights are more valuable
            if thought.get('type') == 'insight' or 'insight' in thought.get('thought', '').lower():
                score += 0.5
                
            # High awareness thoughts are valuable
            score += thought.get('awareness', 0) * 0.3
            
            # Dreams and meditations are ephemeral
            if thought.get('type') in ['dream', 'meditation']:
                score -= 0.4
                
            scored_thoughts.append((thought.get('thought_id', ''), score))
        
        # Sort by score (ascending - worst first)
        scored_thoughts.sort(key=lambda x: x[1])
        
        # Return IDs of thoughts to delete (worst 20%)
        delete_count = max(1, len(scored_thoughts) // 5)
        return [thought_id for thought_id, _ in scored_thoughts[:delete_count]]