#!/bin/bash

echo "🚀 Think AI Language Detection - Local Test"
echo "=========================================="
echo

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test language detection
test_language() {
    local test_name=$1
    local accept_lang=$2
    local message=$3
    local extra_data=$4
    
    echo -e "${BLUE}Test: ${test_name}${NC}"
    echo "Accept-Language: $accept_lang"
    
    if [ -z "$extra_data" ]; then
        response=$(curl -s -X POST http://0.0.0.0:8080/api/chat \
            -H "Content-Type: application/json" \
            -H "Accept-Language: $accept_lang" \
            -d "{\"message\": \"$message\"}")
    else
        response=$(curl -s -X POST http://0.0.0.0:8080/api/chat \
            -H "Content-Type: application/json" \
            -H "Accept-Language: $accept_lang" \
            -d "{\"message\": \"$message\", $extra_data}")
    fi
    
    # Extract language info using grep and sed
    lang_code=$(echo "$response" | grep -o '"code":"[^"]*"' | sed 's/"code":"\([^"]*\)"/\1/')
    lang_name=$(echo "$response" | grep -o '"name":"[^"]*"' | sed 's/"name":"\([^"]*\)"/\1/')
    lang_dir=$(echo "$response" | grep -o '"direction":"[^"]*"' | sed 's/"direction":"\([^"]*\)"/\1/')
    
    if [ ! -z "$lang_code" ]; then
        echo -e "${GREEN}✓ Detected: $lang_name ($lang_code) - Direction: $lang_dir${NC}"
    else
        echo -e "${YELLOW}✗ No language detected in response${NC}"
        echo "Response: $response"
    fi
    echo
}

# Check if server is running
echo "Checking if server is running on port 8080..."
if ! curl -s http://0.0.0.0:8080/health > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Server not running on port 8080${NC}"
    echo
    echo "To start the server, run:"
    echo "  cargo run --bin think-ai-server"
    echo
    echo "Or if you want to run it in the background:"
    echo "  cargo run --bin think-ai-server > server.log 2>&1 &"
    echo
    exit 1
fi

echo -e "${GREEN}✓ Server is running${NC}"
echo

# Run language tests
test_language "Spanish Detection" "es-ES,es;q=0.9,en;q=0.8" "Hola, ¿cómo estás?"

test_language "French Detection" "fr-FR" "Bonjour, comment allez-vous?"

test_language "German with Quality Values" "en;q=0.5,de;q=0.9,es;q=0.8" "Guten Tag"

test_language "Japanese (Explicit)" "en-US" "こんにちは" '"language": "ja"'

test_language "Arabic (RTL)" "ar-SA" "مرحبا"

test_language "Hebrew (RTL)" "he" "שלום"

test_language "Chinese Detection" "zh-CN,zh;q=0.9" "你好"

test_language "Default English" "" "Hello World"

test_language "Invalid Language Fallback" "" "Test" '"language": "xyz"'

echo "=========================================="
echo -e "${GREEN}✓ Testing complete!${NC}"
echo
echo "To test with your own language:"
echo '  curl -X POST http://0.0.0.0:8080/api/chat \'
echo '    -H "Content-Type: application/json" \'
echo '    -H "Accept-Language: YOUR-LANGUAGE-CODE" \'
echo '    -d '"'"'{"message": "Your message"}'"'"