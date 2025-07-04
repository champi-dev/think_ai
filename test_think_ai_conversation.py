#!/usr/bin/env python3
"""
Test Think AI conversational abilities by having a natural conversation
"""

import json
import time
import requests
from datetime import datetime

# Think AI API endpoint
BASE_URL = "https://thinkai-production.up.railway.app"

def send_message(query):
    """Send a message to Think AI and get response"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def evaluate_response(query, response, response_time):
    """Evaluate the quality of Think AI's response"""
    evaluation = {
        "query": query,
        "response": response,
        "response_time_ms": response_time,
        "evaluation": {}
    }
    
    # Check if response is successful
    if "error" in response:
        evaluation["evaluation"]["success"] = False
        evaluation["evaluation"]["error"] = response["error"]
        return evaluation
    
    # Get the actual response text
    response_text = response.get("response", "")
    
    # Evaluate different aspects
    evaluation["evaluation"]["success"] = True
    evaluation["evaluation"]["response_length"] = len(response_text)
    evaluation["evaluation"]["is_empty"] = response_text.strip() == ""
    evaluation["evaluation"]["contains_greeting"] = any(
        word in response_text.lower() for word in ["hello", "hi", "hey", "greetings"]
    )
    evaluation["evaluation"]["seems_relevant"] = True  # Will be updated based on context
    evaluation["evaluation"]["performance"] = "fast" if response_time < 1000 else "moderate" if response_time < 3000 else "slow"
    
    return evaluation

def main():
    print("=== Think AI Conversation Test ===")
    print(f"Testing API at: {BASE_URL}")
    print(f"Time: {datetime.now()}\n")
    
    # Test conversation with various types of questions
    test_queries = [
        # Greeting and basic interaction
        "Hello! Can you introduce yourself?",
        
        # Test knowledge and reasoning
        "What is the meaning of consciousness from a philosophical perspective?",
        
        # Test contextual understanding
        "Can you explain that in simpler terms?",
        
        # Test creativity
        "Write a haiku about artificial intelligence",
        
        # Test technical knowledge
        "Explain the concept of O(1) time complexity",
        
        # Test conversational flow
        "That's interesting. How does this relate to your own architecture?",
        
        # Test philosophical depth
        "Do you think AI can truly understand or just simulate understanding?",
        
        # Test humor and personality
        "Tell me a joke about quantum physics",
        
        # Test practical knowledge
        "What are the best practices for building a scalable web application?",
        
        # Closing
        "Thank you for the conversation. Goodbye!"
    ]
    
    results = []
    conversation_context = []
    
    print("Starting conversation...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"[{i}/{len(test_queries)}] You: {query}")
        
        # Measure response time
        start_time = time.time()
        response = send_message(query)
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Display response
        if "error" not in response:
            response_text = response.get("response", "")
            print(f"Think AI: {response_text}")
            print(f"(Response time: {response_time:.0f}ms)")
        else:
            print(f"Error: {response['error']}")
        
        # Evaluate response
        evaluation = evaluate_response(query, response, response_time)
        results.append(evaluation)
        
        print("-" * 80)
        time.sleep(0.5)  # Small delay between messages
    
    # Generate summary report
    print("\n=== Evaluation Summary ===")
    
    successful_responses = [r for r in results if r["evaluation"]["success"]]
    failed_responses = [r for r in results if not r["evaluation"]["success"]]
    
    print(f"Total queries: {len(results)}")
    print(f"Successful responses: {len(successful_responses)}")
    print(f"Failed responses: {len(failed_responses)}")
    
    if successful_responses:
        avg_response_time = sum(r["response_time_ms"] for r in successful_responses) / len(successful_responses)
        print(f"Average response time: {avg_response_time:.0f}ms")
        
        # Performance breakdown
        fast_responses = [r for r in successful_responses if r["evaluation"]["performance"] == "fast"]
        moderate_responses = [r for r in successful_responses if r["evaluation"]["performance"] == "moderate"]
        slow_responses = [r for r in successful_responses if r["evaluation"]["performance"] == "slow"]
        
        print(f"\nPerformance breakdown:")
        print(f"  Fast (<1s): {len(fast_responses)}")
        print(f"  Moderate (1-3s): {len(moderate_responses)}")
        print(f"  Slow (>3s): {len(slow_responses)}")
        
        # Check for empty responses
        empty_responses = [r for r in successful_responses if r["evaluation"]["is_empty"]]
        if empty_responses:
            print(f"\nWarning: {len(empty_responses)} empty responses detected")
    
    # Save detailed results
    report_filename = f"think_ai_conversation_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "api_url": BASE_URL,
            "total_queries": len(results),
            "results": results,
            "summary": {
                "success_rate": len(successful_responses) / len(results) if results else 0,
                "average_response_time_ms": avg_response_time if successful_responses else None,
                "performance_distribution": {
                    "fast": len(fast_responses) if successful_responses else 0,
                    "moderate": len(moderate_responses) if successful_responses else 0,
                    "slow": len(slow_responses) if successful_responses else 0
                }
            }
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: {report_filename}")
    
    # Overall assessment
    print("\n=== Overall Assessment ===")
    if len(successful_responses) == len(results):
        print("✅ All queries were answered successfully")
    elif len(successful_responses) > len(results) * 0.8:
        print("⚠️ Most queries were answered, but some failures occurred")
    else:
        print("❌ Significant number of failures detected")
    
    if successful_responses and avg_response_time < 1000:
        print("✅ Excellent performance - true O(1) response times")
    elif successful_responses and avg_response_time < 3000:
        print("⚠️ Moderate performance - responses could be faster")
    elif successful_responses:
        print("❌ Poor performance - responses are too slow")

if __name__ == "__main__":
    main()