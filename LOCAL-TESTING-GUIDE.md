# Think AI Local Testing Guide

## 🚀 Quick Start Testing

### 1. **Test the Pre-commit Hook**
```bash
# Test all quality checks without committing
./pre-commit-test.sh
```

### 2. **Build and Test Everything**
```bash
# Build all Rust components
cargo build --release

# Run all tests
cargo test

# Run benchmarks to verify O(1) performance
cargo bench
```

## 🧪 Component-Specific Testing

### Rust Core Engine (O(1) Performance)
```bash
# Unit tests
cargo test -p think-ai-core

# Integration tests
cargo test --test '*'

# Performance benchmarks
cargo bench --bench o1_performance

# Run the O(1) demo
./demo_o1_system.sh
```

### HTTP Server
```bash
# Start the server
./target/release/full-working-o1

# In another terminal, test endpoints
curl http://localhost:8080/health
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello Think AI"}'
```

### Web App (PWA)
```bash
# Start the webapp
./target/release/think-ai-webapp

# Open in browser
open http://localhost:3000

# Test PWA features
# 1. Open DevTools > Application > Service Workers
# 2. Check "Offline" to test offline mode
# 3. Install the PWA from browser
```

### JavaScript Library
```bash
cd think-ai-js

# Install dependencies
npm install

# Run tests
npm test

# Build the library
npm run build

# Test the CLI locally
node dist/cli.js chat
node dist/cli.js ask "What is O(1)?"

# Test as if installed globally
npm link
think-ai chat
```

### Python Library
```bash
cd think-ai-py

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest -v

# Test the CLI
python -m think_ai.cli chat
python -m think_ai.cli ask "What is consciousness?"

# Test the library
python
>>> from think_ai import ThinkAI
>>> ai = ThinkAI()
>>> ai.ask("Hello!")
```

## 🔄 End-to-End Testing

### 1. **Full System Test**
```bash
# Terminal 1: Start the server
./target/release/full-working-o1

# Terminal 2: Test with curl
./test-endpoints.sh

# Terminal 3: Test with JavaScript
cd think-ai-js
npm run test:integration

# Terminal 4: Test with Python
cd think-ai-py
python test_integration.py
```

### 2. **Create Test Scripts**

**test-endpoints.sh:**
```bash
#!/bin/bash
# Test all API endpoints

echo "Testing Think AI Endpoints..."

# Health check
echo -n "Health check: "
curl -s http://localhost:8080/health | jq .

# Chat endpoint
echo -n "Chat test: "
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is O(1)?"}' | jq .

# Stats endpoint
echo -n "Stats test: "
curl -s http://localhost:8080/api/stats | jq .

# Search endpoint
echo -n "Search test: "
curl -s "http://localhost:8080/api/search?query=consciousness&limit=5" | jq .
```

### 3. **Performance Testing**
```bash
# Run O(1) performance tests
cargo run --release --bin o1_performance_test

# Benchmark with Apache Bench
ab -n 1000 -c 10 http://localhost:8080/health

# Load test with hey
hey -n 10000 -c 100 http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

## 🐳 Docker Testing

```bash
# Build Docker image
docker build -t think-ai-test .

# Run container
docker run -p 8080:8080 think-ai-test

# Test from host
curl http://localhost:8080/health
```

## 🧩 Library Integration Testing

### JavaScript Test Script
```javascript
// test-integration.js
const { ThinkAI } = require('./think-ai-js');

async function test() {
  const ai = new ThinkAI({ 
    baseUrl: 'http://localhost:8080',
    debug: true 
  });
  
  // Test chat
  const response = await ai.chat({
    query: "What is O(1) performance?"
  });
  console.log('Chat response:', response);
  
  // Test streaming
  await ai.streamChat(
    { query: "Tell me about consciousness" },
    (chunk) => process.stdout.write(chunk.chunk || '')
  );
  
  // Test stats
  const stats = await ai.getStats();
  console.log('Stats:', stats);
}

test().catch(console.error);
```

### Python Test Script
```python
# test_integration.py
from think_ai import ThinkAI, ChatRequest

def test():
    ai = ThinkAI()
    
    # Test chat
    response = ai.chat(ChatRequest(
        query="What is O(1) performance?"
    ))
    print(f"Response: {response.response}")
    print(f"Confidence: {response.confidence}")
    print(f"Time: {response.response_time_ms}ms")
    
    # Test streaming
    def print_chunk(chunk):
        print(chunk.chunk, end='', flush=True)
    
    ai.stream_chat(
        ChatRequest(query="Tell me about consciousness"),
        print_chunk
    )
    
    # Test search
    results = ai.search("quantum", limit=5)
    for result in results:
        print(f"- {result.content} (score: {result.score})")

if __name__ == "__main__":
    test()
```

## 🔍 Debugging Tips

### 1. **Enable Debug Logging**
```bash
# Rust
RUST_LOG=debug cargo run

# JavaScript
DEBUG=* node dist/cli.js chat

# Python
python -m think_ai.cli --debug chat
```

### 2. **Check Port Availability**
```bash
# Kill processes on port 8080
lsof -ti:8080 | xargs kill -9

# Or use the helper
./kill-port.sh 8080
```

### 3. **Monitor Performance**
```bash
# Watch CPU and memory
htop

# Monitor network traffic
sudo tcpdump -i lo0 port 8080

# Check response times
time curl http://localhost:8080/health
```

## ✅ Testing Checklist

- [ ] Pre-commit hooks pass (`./pre-commit-test.sh`)
- [ ] Rust tests pass (`cargo test`)
- [ ] O(1) benchmarks confirm performance (`cargo bench`)
- [ ] Server starts and responds (`curl http://localhost:8080/health`)
- [ ] Web app loads and works offline
- [ ] JavaScript CLI works (`npx think-ai chat`)
- [ ] Python CLI works (`think-ai chat`)
- [ ] Streaming works in both libraries
- [ ] Docker build succeeds
- [ ] All endpoints return < 100ms

## 🎯 Expected Performance

When everything is working correctly:
- Health checks: < 1ms
- Chat responses: < 50ms
- Search queries: < 20ms
- Stats retrieval: < 5ms
- Memory usage: < 100MB
- CPU usage: < 5% idle

## 🚨 Common Issues

1. **Port already in use**
   ```bash
   ./kill-port.sh 8080
   ```

2. **Rust version mismatch**
   ```bash
   rustup update
   rustup default stable
   ```

3. **Missing dependencies**
   ```bash
   # JavaScript
   cd think-ai-js && npm install
   
   # Python
   cd think-ai-py && pip install -e ".[dev]"
   ```

4. **WebSocket connection failed**
   - Check if server supports WebSocket
   - Ensure no proxy is blocking WebSocket

---

Remember: The goal is to verify O(1) performance at every level!