#!/usr/bin/env python3
"""
Test the improved AI server responses
"""
import json
from improved_ai_server import ImprovedKnowledgeMatcher

def test_responses():
    matcher = ImprovedKnowledgeMatcher()
    
    test_queries = [
        "what is love",
        "tell me about love",
        "explain love to me", 
        "ping",
        "what is quantum physics",
        "tell me about electrical engineering",
        "explain psycholinguistics",
        "what is the meaning of life",  # Unknown query
        "how does photosynthesis work",  # Unknown query
    ]
    
    print("Testing Improved AI Response Matching\n" + "="*50)
    
    for query in test_queries:
        response = matcher.find_best_match(query)
        print(f"\nQuery: '{query}'")
        print(f"Response preview: {response[:150]}...")
        
        # Check if response is relevant
        query_lower = query.lower()
        response_lower = response.lower()
        
        if "love" in query_lower:
            if "love" in response_lower or "affection" in response_lower or "emotion" in response_lower:
                print("✅ Response is relevant to love")
            else:
                print("❌ Response is NOT relevant to love")
        elif "quantum" in query_lower:
            if "quantum" in response_lower or "physics" in response_lower:
                print("✅ Response is relevant to quantum physics")
            else:
                print("❌ Response is NOT relevant to quantum physics")
        elif "electrical" in query_lower:
            if "electrical" in response_lower or "engineering" in response_lower:
                print("✅ Response is relevant to electrical engineering")  
            else:
                print("❌ Response is NOT relevant to electrical engineering")
        elif "psycholinguistics" in query_lower:
            if "psycholinguistics" in response_lower or "language" in response_lower:
                print("✅ Response is relevant to psycholinguistics")
            else:
                print("❌ Response is NOT relevant to psycholinguistics")
        else:
            if "don't have specific information" in response_lower:
                print("✅ Correctly handled unknown query")
            else:
                print("⚠️  Response for unknown query")

if __name__ == "__main__":
    test_responses()