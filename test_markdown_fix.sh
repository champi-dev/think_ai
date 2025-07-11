#!/bin/bash

echo "🚀 Testing Markdown Fix for Think AI"
echo "===================================="

# Start the server on port 3456
echo "Starting server on port 3456..."
PORT=3456 ./target/release/full-working-o1 &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 5

# Check if server is running
if ! curl -s http://localhost:3456/health >/dev/null 2>&1; then
    echo "❌ Server failed to start"
    exit 1
fi

echo "✅ Server started successfully on port 3456"
echo ""
echo "📝 Testing markdown rendering..."
echo ""

# Test message with complex markdown
TEST_MESSAGE='Sure! Here are some Python scripts that cover a variety of topics in different areas of science.

## 1. Simple Calculator

A basic calculator for performing arithmetic operations.

```python
def simple_calculator():
    print("Simple Calculator")
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))
    
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error! Division by zero"
    else:
        result = "Invalid operator"
    
    print(f"Result: {result}")

simple_calculator()
```

## 2. Temperature Conversion

Convert temperatures between Celsius and Fahrenheit.

```python
def temperature_converter():
    print("Temperature Converter")
    unit = input("Enter C for Celsius or F for Fahrenheit: ").upper()
    
    if unit == "C":
        celsius = float(input("Enter temperature in Celsius: "))
        fahrenheit = (celsius * 9/5) + 32
        print(f"{celsius}°C is {fahrenheit:.2f}°F")
    elif unit == "F":
        fahrenheit = float(input("Enter temperature in Fahrenheit: "))
        celsius = (fahrenheit - 32) * 5/9
        print(f"{fahrenheit}°F is {celsius:.2f}°C")
    else:
        print("Invalid input")

temperature_converter()
```

## 3. Fibonacci Sequence

Generate the Fibonacci sequence up to n terms.

- This demonstrates iteration
- Shows basic math operations  
- Uses lists to store results

1. Start with 0 and 1
2. Add previous two numbers
3. Continue for n terms

**Note**: This is a classic programming example that shows *recursion* and **dynamic programming** concepts.'

# Send test request
echo "Sending test request..."
RESPONSE=$(curl -s -X POST http://localhost:3456/chat \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Show me the markdown test\"}")

echo "Response received:"
echo "$RESPONSE" | jq -r '.response' 2>/dev/null || echo "$RESPONSE"
echo ""

# Open browser to test visual rendering
echo "Opening browser to test visual rendering..."
echo "Please check: http://localhost:3456/static/chat.html"
echo ""
echo "Instructions for testing:"
echo "1. Open the chat interface"
echo "2. Send a message asking for Python code examples"
echo "3. Verify that:"
echo "   - Code blocks are properly formatted with syntax highlighting"
echo "   - Headers are displayed correctly"
echo "   - Lists show proper indentation"
echo "   - Bold and italic text work"
echo "   - Line breaks and paragraphs are preserved"
echo ""
echo "Server is running on PID: $SERVER_PID"
echo "To stop the server, run: kill $SERVER_PID"
echo ""
echo "To test manually, try sending this message in the chat:"
echo '```'
echo 'Show me Python examples with:
# Headers
**Bold text**
*Italic text*
- Bullet lists
1. Numbered lists

```python
def test():
    return "code block"
```'
echo '```'