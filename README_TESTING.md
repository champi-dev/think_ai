# Testing Think AI Locally

## Quick Start

```bash
# Build the project
cargo build --release

# Start the server
./target/release/full-server
```

## Testing Methods

### 1. HTTP API (Server Mode)
```bash
# Start server (port 8080)
./target/release/full-server

# In another terminal, test with curl:
# Simple query
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the sun?"}'

# Test context awareness
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the sun?"}'

curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is it made of?"}'

# Check server stats
curl http://localhost:8080/api/stats
```

### 2. CLI Mode (Interactive)
```bash
# Start interactive chat
./target/release/think-ai chat

# Example queries:
> What is Mars?
> Tell me about TinyLlama
> What is consciousness?
```

### 3. Automated Test Scripts
```bash
# Run basic tests
./test_quantum_llm.sh

# Test specific functionality
./test_dynamic_responses.sh
./test_context_awareness.sh
```

### 4. Web Interface
```bash
# Start the webapp (includes 3D visualization)
./target/release/think-ai-webapp

# Open browser to http://localhost:8080
```

## Adding Custom Knowledge

1. Create a JSON file in the `knowledge/` directory:

```json
{
  "domain": "astronomy",
  "entries": [
    {
      "topic": "jupiter",
      "content": "Jupiter is the largest planet in our solar system...",
      "related_concepts": ["planet", "gas giant", "solar system"],
      "metadata": {
        "size": "139,820 km diameter",
        "moons": "95 known moons"
      }
    }
  ]
}
```

2. Restart the server to load new knowledge

## Troubleshooting

- **Port already in use**: `lsof -ti:8080 | xargs kill -9`
- **Build errors**: `cargo clean && cargo build --release`
- **Missing knowledge**: Check `knowledge/` directory exists with JSON files
- **Slow responses**: Ensure release build with `--release` flag

## Performance Testing

```bash
# Benchmark response times
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# Expected: < 1ms response time (O(1) performance)
```