# Think AI Persistent Chat - Manual Testing Guide

## Quick Start

1. **Kill any existing processes on port 8080:**
   ```bash
   lsof -ti:8080 | xargs kill -9 2>/dev/null || true
   ```

2. **Start the server:**
   ```bash
   ./target/release/think-ai-full-persistent
   ```

3. **Open your browser:**
   - Navigate to: http://localhost:8080
   - You should see the 3D visualization interface

## Testing Persistent Conversations

### Test 1: Basic Context Retention
1. Send a message introducing yourself:
   ```
   "Hi, my name is [Your Name] and I work as a [Your Job]"
   ```

2. Send a follow-up message:
   ```
   "What's my name?"
   ```

3. **Expected:** The AI should remember your name from the first message

### Test 2: Multi-Turn Conversations
1. Start a topic:
   ```
   "I want to learn about quantum computing"
   ```

2. Ask follow-up questions:
   ```
   "Can you explain qubits?"
   "How does superposition work?"
   "What did we start talking about?"
   ```

3. **Expected:** The AI maintains context throughout the conversation

### Test 3: Session Persistence
1. Note your session ID (shown in responses or browser console)
2. Refresh the browser
3. Continue the conversation
4. **Expected:** The conversation history should be maintained

### Test 4: Delete History
1. Send the command:
   ```
   "delete my history"
   ```

2. **Expected:** 
   - You'll get a confirmation message
   - A new session ID will be created
   - Previous conversation context will be gone

### Test 5: Concurrent Sessions
1. Open two different browser windows/tabs
2. Start different conversations in each
3. **Expected:** Each session maintains its own separate context

## API Testing with cURL

### Send a message:
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, my name is Alice"}'
```

### Continue with session ID:
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is my name?", "session_id": "YOUR_SESSION_ID"}'
```

### Delete history:
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "delete my history", "session_id": "YOUR_SESSION_ID"}'
```

## Performance Testing

1. **Response Time:** Messages should respond in under 1 second
2. **Memory Usage:** Monitor with `htop` or `top` during extended conversations
3. **Concurrent Load:** Try multiple simultaneous conversations

## What to Look For

✅ **Working Correctly:**
- AI remembers information from earlier in the conversation
- Each session maintains separate context
- Delete command clears history and creates new session
- Fast response times (< 1s)

❌ **Issues to Report:**
- AI forgets information between messages
- Sessions interfere with each other
- Delete command doesn't work
- Slow responses or timeouts
- Server crashes

## Troubleshooting

1. **Server won't start:**
   - Check if port 8080 is already in use
   - Run: `lsof -i:8080` to see what's using it

2. **No responses:**
   - Check server logs in the terminal
   - Ensure Qwen API is configured correctly

3. **Context not retained:**
   - Check if session ID is being passed correctly
   - Look for errors in server logs

## Advanced Testing

### Test Long Conversations
Try having a 20+ message conversation to test:
- Memory limits
- Performance degradation
- Context window handling

### Test Special Characters
Send messages with:
- Emojis 😊
- Special characters: @#$%^&*
- Multi-line messages
- Very long messages (1000+ characters)

### Test Error Scenarios
- Invalid JSON to the API
- Missing session IDs
- Concurrent delete commands