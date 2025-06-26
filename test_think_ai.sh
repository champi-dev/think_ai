#!/bin/bash

# Think AI Local Testing Script
echo "🤖 Think AI Test Suite"
echo "====================="

API="http://localhost:8080/api/chat"

# Function to send query and display response
ask() {
    echo -e "\n❓ Question: $1"
    response=$(curl -s -X POST $API -H "Content-Type: application/json" -d "{\"query\": \"$1\"}" | jq -r '.response')
    echo "💬 Response: $response"
}

# Test 1: Greeting
echo -e "\n📌 Test 1: Greeting"
ask "hello"

# Test 2: Sun queries with context
echo -e "\n📌 Test 2: Sun (with context awareness)"
ask "what is the sun"
ask "what is it made of"
ask "how big is it"

# Test 3: Mars queries with context
echo -e "\n📌 Test 3: Mars (with context awareness)"
ask "tell me about mars"
ask "does it have water"

# Test 4: Other queries
echo -e "\n📌 Test 4: Various topics"
ask "what is consciousness"
ask "what is quantum mechanics"
ask "what is AI"

echo -e "\n✅ Test complete!"