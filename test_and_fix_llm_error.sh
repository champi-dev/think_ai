#!/bin/bash

echo "=== Testing and Fixing 'Knowledge engine LLM not initialized' Error ==="
echo

# First, let's test the current behavior
echo "1. Testing current behavior with a scientific query..."
echo

curl -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "explain the theory of relativity"
  }' 2>/dev/null | jq -r '.response' | head -n 2

echo
echo "2. Testing with a philosophical query..."
echo

curl -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "what is the meaning of existence"
  }' 2>/dev/null | jq -r '.response' | head -n 2

echo
echo "3. Testing with a technical query..."
echo

curl -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "explain how computers work"
  }' 2>/dev/null | jq -r '.response' | head -n 2

echo
echo "The issue: Several response components are trying to use knowledge_engine.generate_llm_response()"
echo "which returns 'Knowledge engine LLM not initialized' because the quantum_llm is not set up."
echo
echo "This is due to a circular dependency between KnowledgeEngine and EnhancedQuantumLLMEngine."
echo
echo "To fix this, we need to modify the response components to provide their own responses"
echo "instead of delegating to the non-existent LLM engine."