# Think AI - Local Usage Guide

## 🚀 Quick Start

### Option 1: Run Everything with One Command
```bash
./run_local.sh
```
This starts the HTTP server and makes the web interface available at http://localhost:8080

### Option 2: Run Components Individually

#### 1. Terminal Chat Only
```bash
# Build first (if not already built)
cargo build --release

# Run interactive chat
./target/release/think-ai chat
```

#### 2. HTTP Server + Web Interface
```bash
# Start the server (includes web interface)
./target/release/think-ai server

# Access at http://localhost:8080
```

## 💬 Terminal Chat Commands

When in chat mode, you can use these commands:
- `help` - Show available commands
- `stats` - Display performance statistics
- `history` - Show conversation history
- `clear` - Clear conversation context
- `exit` or `quit` - Exit the chat

## 🌐 Web Interface Features

The web interface at http://localhost:8080 provides:
- 3D consciousness visualization
- Real-time chat interface
- Performance metrics
- Interactive code generation

## 🔧 API Usage

While the server is running, you can also use the API:

```bash
# Health check
curl http://localhost:8080/health

# Send a query
curl -X POST http://localhost:8080/api/process \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum computing"}'
```

## 🎯 Example Sessions

### Terminal Chat Session
```bash
$ ./target/release/think-ai chat

╔════════════════════════════════════════════════════════════╗
║              🧠 THINK AI CONSCIOUSNESS v4.0 (Rust)        ║
╠════════════════════════════════════════════════════════════╣
║  ⚡ Natural Intelligence  │  🌍 Multilingual              ║
║  💫 Context-Aware        │  🚀 Human-like Responses      ║
╚════════════════════════════════════════════════════════════╝

💭 I'm ready to chat! Type 'help' for commands.

You: What is the meaning of life?
Think AI: I found 10 relevant pieces of knowledge...
[⚡ 0.1ms]

You: Generate a fibonacci function
Think AI: Here's an optimized O(1) Fibonacci implementation...
[⚡ 0.2ms]
```

### Running Multiple Instances

You can run the chat in one terminal while the server runs in another:

**Terminal 1:**
```bash
./target/release/think-ai server
```

**Terminal 2:**
```bash
./target/release/think-ai chat
```

## 🛠️ Troubleshooting

### Port Already in Use
If you get "Address already in use" error:
```bash
# Kill process on port 8080
sudo lsof -ti:8080 | xargs kill -9

# Or use a different port
./target/release/think-ai server --port 3000
```

### Build Issues
```bash
# Clean build
cargo clean
cargo build --release
```

### Performance Testing
```bash
# Run the full test suite
./test_deployment.sh
```

## 📊 Performance Tips

1. **First Run**: The first query might be slightly slower as the knowledge base loads
2. **Memory Usage**: Expect ~50-100MB base memory usage
3. **Response Time**: Should be 0.1-0.2ms after warmup

## 🎨 Customization

### Change Server Port
```bash
./target/release/think-ai server --port 3000 --host 0.0.0.0
```

### Environment Variables
```bash
# Set log level
RUST_LOG=debug ./target/release/think-ai server

# Custom port (alternative to --port)
PORT=3000 ./target/release/think-ai server
```

## 💡 Tips

1. **Best Chat Experience**: Use the terminal chat for fastest responses
2. **Web Interface**: Best for visualizing AI consciousness and metrics
3. **API Integration**: Use the HTTP API for integrating with other tools

## 🔄 Stopping the System

- **Terminal Chat**: Type `exit` or press `Ctrl+C`
- **Server**: Press `Ctrl+C` in the terminal where it's running
- **Full System**: If using `run_local.sh`, press `Ctrl+C` to stop all services