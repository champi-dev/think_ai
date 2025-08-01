#!/usr/bin/env python3
"""
Enhance Think AI knowledge to be more conversational and direct
"""

import json
import os
from pathlib import Path
import re

class ConversationalEnhancer:
    def __init__(self):
        self.knowledge_dir = Path("/home/administrator/think_ai/knowledge_files")
        self.conversational_templates = {
            "direct": [
                "{content}",
                "Here's what you need to know: {content}",
                "Simply put, {content}",
                "The answer is straightforward: {content}",
                "{content} That's the core of it.",
                "Let me explain directly: {content}",
                "In practical terms: {content}",
                "Here's the deal: {content}",
                "To put it plainly: {content}",
                "The key point is this: {content}"
            ],
            "helpful": [
                "{content} I hope this helps clarify things!",
                "{content} Does this make sense?",
                "{content} Let me know if you need more details.",
                "{content} Feel free to ask for clarification.",
                "{content} I can elaborate if needed.",
                "Great question! {content}",
                "I'm glad you asked. {content}",
                "That's an interesting topic. {content}",
                "Good thinking! {content}",
                "Excellent question. {content}"
            ],
            "engaging": [
                "You know what's fascinating? {content}",
                "Here's something cool: {content}",
                "This is really interesting: {content}",
                "Want to know something neat? {content}",
                "Check this out: {content}",
                "Here's the interesting part: {content}",
                "What's really cool is that {content}",
                "The amazing thing is: {content}",
                "Fun fact: {content}",
                "Here's what's remarkable: {content}"
            ]
        }
        
        self.simplification_rules = [
            # Academic to conversational
            ("encompasses", "includes"),
            ("utilizes", "uses"),
            ("demonstrates", "shows"),
            ("indicates", "means"),
            ("constitutes", "is"),
            ("represents", "is"),
            ("comprises", "includes"),
            ("pertains to", "relates to"),
            ("in accordance with", "following"),
            ("with regard to", "about"),
            ("in order to", "to"),
            ("due to the fact that", "because"),
            ("at this point in time", "now"),
            ("in the event that", "if"),
            ("prior to", "before"),
            ("subsequent to", "after"),
            ("is capable of", "can"),
            ("has the ability to", "can"),
            ("is in a position to", "can"),
            # Make it more direct
            ("It should be noted that", "Note that"),
            ("It is important to understand that", "Understand that"),
            ("One must consider", "Consider"),
            ("It has been observed that", "We've seen that"),
            ("Research indicates", "Studies show"),
            ("Evidence suggests", "It appears"),
            ("It is believed that", "We think"),
            ("It is known that", "We know"),
            # Remove hedging
            ("somewhat", ""),
            ("relatively", ""),
            ("quite", ""),
            ("rather", ""),
            ("fairly", ""),
            ("It seems that", ""),
            ("It appears that", ""),
            ("arguably", ""),
            ("potentially", "possibly"),
        ]

    def make_conversational(self, text):
        """Transform text to be more conversational"""
        # Apply simplification rules
        result = text
        for formal, simple in self.simplification_rules:
            result = re.sub(r'\b' + formal + r'\b', simple, result, flags=re.IGNORECASE)
        
        # Remove double spaces
        result = re.sub(r'\s+', ' ', result).strip()
        
        # Make sentences shorter
        sentences = result.split('. ')
        if len(sentences) > 3:
            # Keep only the most important sentences
            key_sentences = []
            for sent in sentences:
                if any(word in sent.lower() for word in ['is', 'are', 'means', 'includes', 'helps', 'enables', 'allows']):
                    key_sentences.append(sent)
            if key_sentences:
                result = '. '.join(key_sentences[:3]) + '.'
        
        return result

    def enhance_entry(self, entry):
        """Enhance a single knowledge entry to be more conversational"""
        original_content = entry.get("content", "")
        
        # Make the content more conversational
        conversational_content = self.make_conversational(original_content)
        
        # Create diverse conversational patterns
        new_patterns = []
        
        # Add direct patterns
        for template in self.conversational_templates["direct"][:3]:
            pattern = template.format(content=conversational_content)
            new_patterns.append(pattern)
        
        # Add helpful patterns
        for template in self.conversational_templates["helpful"][:3]:
            pattern = template.format(content=conversational_content)
            new_patterns.append(pattern)
        
        # Add engaging patterns
        for template in self.conversational_templates["engaging"][:4]:
            pattern = template.format(content=conversational_content)
            new_patterns.append(pattern)
        
        # Update the entry
        entry["content"] = conversational_content
        entry["metadata"]["conversational_patterns"] = new_patterns
        entry["metadata"]["enhanced"] = True
        
        return entry

    def enhance_domain(self, domain_file):
        """Enhance all entries in a domain file"""
        with open(domain_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        enhanced_entries = []
        for entry in data.get("entries", []):
            enhanced_entry = self.enhance_entry(entry)
            enhanced_entries.append(enhanced_entry)
        
        data["entries"] = enhanced_entries
        if "metadata" not in data:
            data["metadata"] = {}
        data["metadata"]["conversational_enhancement"] = True
        
        # Save the enhanced version
        with open(domain_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return len(enhanced_entries)

    def enhance_all_knowledge(self):
        """Enhance all knowledge files to be more conversational"""
        print("🎯 Enhancing Think AI Knowledge for Better Conversations")
        print("=" * 60)
        
        total_enhanced = 0
        
        for json_file in self.knowledge_dir.glob("*.json"):
            if json_file.name == "knowledge_index.json":
                continue
            
            print(f"\n📝 Enhancing {json_file.name}...")
            count = self.enhance_domain(json_file)
            total_enhanced += count
            print(f"   ✅ Enhanced {count} entries")
        
        # Update response cache with conversational responses
        self.update_response_cache()
        
        print("\n" + "=" * 60)
        print(f"✨ Enhancement complete!")
        print(f"📊 Total entries enhanced: {total_enhanced}")
        print(f"🎯 Knowledge is now more conversational and direct!")

    def update_response_cache(self):
        """Update the response cache with conversational patterns"""
        cache_dir = Path("/home/administrator/think_ai/cache")
        cache_file = cache_dir / "response_cache.json"
        
        new_cache = {}
        
        # Common queries and conversational responses
        common_queries = {
            "hello": "Hey there! I'm Think AI, ready to help you with anything you need. What's on your mind?",
            "hi": "Hi! Great to meet you. What can I help you with today?",
            "how are you": "I'm doing great, thanks for asking! Ready to assist you. What would you like to know?",
            "what can you do": "I can help with pretty much anything! Science, technology, philosophy, practical advice - you name it. What interests you?",
            "help": "I'm here to help! Just ask me anything - whether it's about quantum physics, cooking tips, or life advice. What do you need?",
            "thanks": "You're welcome! Happy to help. Anything else you'd like to know?",
            "thank you": "My pleasure! Feel free to ask me anything else.",
            "bye": "Take care! Come back anytime you need help.",
            "goodbye": "Goodbye! It was great chatting with you. Have an awesome day!",
        }
        
        # Add common queries
        for query, response in common_queries.items():
            key = hashlib.md5(query.encode()).hexdigest()
            new_cache[key] = {
                "response": response,
                "timestamp": time.time(),
                "confidence": 1.0
            }
        
        # Merge with existing cache
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                existing = json.load(f)
                new_cache.update(existing)
        
        # Save updated cache
        with open(cache_file, 'w') as f:
            json.dump(new_cache, f, indent=2)
        
        print(f"\n✅ Updated response cache with {len(new_cache)} entries")

import hashlib
import time

def main():
    enhancer = ConversationalEnhancer()
    enhancer.enhance_all_knowledge()
    
    print("\n🚀 To use the enhanced knowledge:")
    print("1. Restart the service: sudo systemctl restart think-ai-main")
    print("2. The AI will now respond more naturally and directly!")

if __name__ == "__main__":
    main()