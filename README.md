# 🧠 Think AI

> A quantum-powered AI system with O(1) performance, consciousness-driven responses, and autonomous capabilities

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Rust](https://img.shields.io/badge/rust-1.70%2B-orange.svg)](https://www.rust-lang.org/)
[![Node](https://img.shields.io/badge/node-18%2B-green.svg)](https://nodejs.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](docs/TESTING.md)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](docs/TESTING.md)

Think AI is an advanced artificial intelligence system that combines quantum-inspired algorithms with a consciousness framework to deliver intelligent, context-aware responses. Now featuring **autonomous agent capabilities** that allow parallel background processing while prioritizing human assistance.

🌐 **Live Demo**: [https://thinkai.lat](https://thinkai.lat)  
📊 **Metrics Dashboard**: [https://thinkai.lat/stats](https://thinkai.lat/stats)  
🎯 **WhatsApp Integration**: Send messages to get AI responses via WhatsApp  
🔊 **Audio Support**: Voice transcription and synthesis with Deepgram/ElevenLabs

## ✨ Features

### Core Capabilities
- **🚀 O(1) Performance**: Constant-time algorithms for scalable AI operations
- **🤖 Autonomous Agent**: Self-improving system that runs tasks in parallel
- **🧩 Modular Architecture**: Microservice-inspired design with specialized crates
- **💭 Consciousness Framework**: Self-aware system with metacognitive capabilities
- **📚 Knowledge Transfer**: Sophisticated learning and adaptation mechanisms
- **🔍 Semantic Search**: Vector-based similarity search for relevant context
- **💾 Eternal Memory**: Session persistence with conversation history
- **📈 Real-time Metrics**: Comprehensive monitoring with memory leak protection

### Autonomous Agent Features (NEW!)
- **🎯 Human-First Priority**: Always prioritizes human requests above all else
- **🔄 Self-Improvement**: Analyzes performance and optimizes continuously
- **📖 Knowledge Gathering**: Researches topics autonomously in background
- **🛡️ Safety Mechanisms**: Never interferes with systemd or critical processes
- **📝 Activity Logging**: Full transparency with detailed activity logs
- **🧠 Model Switching**: Uses Qwen/CodeLlama based on task requirements

### User Features
- **📱 Responsive UI**: Works seamlessly on desktop, tablet, and mobile
- **💻 Code Mode**: Specialized mode for programming assistance
- **🔎 Web Search**: Real-time web search integration
- **✓ Fact Checking**: Built-in fact verification system
- **🌊 Streaming Responses**: Real-time response streaming via SSE/WebSocket
- **📦 PWA Support**: Installable as a native app with offline capabilities
- **🎤 Voice Interface**: Speak to AI and receive audio responses
- **💬 WhatsApp Bot**: Chat with ThinkAI through WhatsApp

## 🏗️ Architecture

Think AI uses a modern full-stack architecture with autonomous capabilities:

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (React)                   │
│  ┌─────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐  │
│  │   UI    │ │   PWA    │ │  SSE  │ │    WS    │  │
│  └─────────┘ └──────────┘ └───────┘ └──────────┘  │
└─────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────┐
│                  Backend (Rust/Axum)                 │
│  ┌─────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐  │
│  │   API   │ │ Sessions │ │ Auth  │ │  Metrics │  │
│  └─────────┘ └──────────┘ └───────┘ └──────────┘  │
│  ┌─────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐  │
│  │  Audio  │ │ WhatsApp │ │ Cache │ │Autonomous│  │
│  └─────────┘ └──────────┘ └───────┘ └──────────┘  │
└─────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────┐
│              Core AI Components (Rust)               │
│  ┌─────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐  │
│  │  Qwen   │ │CodeLlama │ │Vector │ │Knowledge │  │
│  └─────────┘ └──────────┘ └───────┘ └──────────┘  │
│  ┌─────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐  │
│  │Quantum  │ │Conscious │ │Storage│ │  Utils   │  │
│  └─────────┘ └──────────┘ └───────┘ └──────────┘  │
└─────────────────────────────────────────────────────┘
```

## 📦 Components

### Core Crates
- **think-ai-core**: Core O(1) engine and quantum algorithms
- **think-ai-consciousness**: Self-awareness and metacognitive processing
- **think-ai-knowledge**: Knowledge management with dynamic learning
- **think-ai-vector**: High-performance vector operations
- **think-ai-qwen**: Qwen model integration (3B parameter model)
- **think-ai-codellama**: CodeLlama integration for code generation
- **think-ai-storage**: Persistent storage with RocksDB backend
- **think-ai-utils**: Shared utilities and helpers

### Frontend
- **React 18**: Modern UI with hooks and concurrent features
- **Tailwind CSS**: Utility-first styling
- **Zustand**: State management
- **PWA**: Progressive Web App with offline support

### Backend Services
- **Axum**: High-performance web framework
- **Tower**: Middleware and service composition
- **Metrics**: Real-time monitoring with memory leak protection
- **Audio Service**: Deepgram transcription + ElevenLabs synthesis
- **WhatsApp Integration**: Twilio-powered messaging

## 🚀 Quick Start

### Prerequisites
- Rust 1.70+ with cargo
- Node.js 18+ with npm
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/champi-dev/think_ai.git
cd think_ai
```

2. Install dependencies:
```bash
# Backend
cargo build --release

# Frontend
cd frontend
npm install
```

3. Set up environment variables:
```bash
# Copy example env file
cp .env.example .env

# Add your API keys:
# - DEEPGRAM_API_KEY for audio transcription
# - ELEVENLABS_API_KEY for voice synthesis
# - TWILIO_* for WhatsApp integration
# - GEMINI_API_KEY for enhanced responses (optional)
```

4. Run the system:
```bash
# Start backend (with autonomous agent)
cargo run --release --bin think-ai-autonomous

# In another terminal, start frontend
cd frontend
npm start
```

5. Access the application:
- Web UI: http://localhost:3000
- API: http://localhost:7777
- Metrics: http://localhost:7777/stats
- Autonomous Status: http://localhost:7777/api/autonomous/status

## 🤖 Autonomous Agent

The autonomous agent runs in the background, continuously improving and learning:

### Enable Autonomous Mode
```bash
ENABLE_AUTONOMOUS=true cargo run --release --bin think-ai-autonomous
```

### Submit Tasks to Agent
```bash
curl -X POST http://localhost:7777/api/autonomous/task \
  -H "Content-Type: application/json" \
  -d '{"request": "Research quantum computing applications"}'
```

### Monitor Agent Activity
```bash
# Check status
curl http://localhost:7777/api/autonomous/status

# View logs
journalctl -u thinkai-autonomous -f
```

## 📊 Metrics Dashboard

Access real-time metrics at `/stats`:
- Request counts and response times
- CPU and memory usage
- Audio transcription/synthesis stats
- WhatsApp message counts
- Error tracking with detailed logs
- Endpoint performance analytics

## 🎯 Production Deployment

### Using SystemD
```bash
# Copy service file
sudo cp deploy/thinkai.service /etc/systemd/system/

# Enable and start
sudo systemctl enable thinkai
sudo systemctl start thinkai
```

### Using Docker
```bash
# Build image
docker build -t thinkai .

# Run container
docker run -p 7777:7777 -p 3000:3000 thinkai
```

### Environment Variables
```bash
# Required for production
PORT=7777
RUST_LOG=info
DEEPGRAM_API_KEY=your_key
ELEVENLABS_API_KEY=your_key

# Optional
ENABLE_AUTONOMOUS=true
ENABLE_WHATSAPP=true
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## 📖 Documentation

- [API Documentation](docs/API.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Autonomous Agent Guide](docs/AUTONOMOUS_AGENT.md)
- [Testing Guide](docs/TESTING.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## 🧪 Testing

```bash
# Run all tests
cargo test

# Run with coverage
cargo tarpaulin --out Html

# E2E tests
npm run test:e2e
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Qwen team for the amazing 3B model
- CodeLlama team for code generation capabilities
- Deepgram for speech recognition
- ElevenLabs for voice synthesis
- The Rust and React communities

## 📞 Contact

- **Email**: danielsarcor@gmail.com
- **GitHub**: [@champi-dev](https://github.com/champi-dev)
- **Live Demo**: [thinkai.lat](https://thinkai.lat)

---

Built with ❤️ by the Think AI team. Now with autonomous capabilities for continuous self-improvement!