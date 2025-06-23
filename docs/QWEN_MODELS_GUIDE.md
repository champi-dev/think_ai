# Qwen Models Integration Guide

This guide explains how to use lightweight Qwen models in Think AI for different tasks.

## Overview

Think AI now supports multiple model providers with task-specific model selection. The system automatically chooses the most appropriate Qwen model based on your task:

- **Chat**: General conversation and Q&A
- **Coding**: Code generation and programming help  
- **Math**: Mathematical problem solving
- **Multimodal**: Vision + text understanding
- **Reasoning**: Complex logical reasoning

## Quick Start

### 1. Install Ollama

First, install Ollama from [ollama.com](https://ollama.com/download).

### 2. Setup Qwen Models

Run the setup script to install lightweight models:

```bash
./scripts/setup_qwen_models.sh
```

This installs:
- `qwen2.5:0.5b` - Ultra-fast chat (0.5B parameters)
- `qwen2.5:1.5b` - Fast general chat (1.5B parameters)
- `qwen2.5-coder:1.5b` - Fast code generation

### 3. Test the Integration

Run the demo to see different models in action:

```bash
python examples/qwen_models_demo.py
```

## Model Recommendations

### Minimal Setup (Fast Responses)
Perfect for quick interactions and low-resource environments:
- `qwen2.5:0.5b` - Simple queries, basic chat
- `qwen2.5:1.5b` - General purpose chat
- `qwen2.5-coder:1.5b` - Basic code generation

### Balanced Setup (Good Quality + Speed)
Best for most use cases:
- `qwen2.5:3b` - High-quality chat
- `qwen2.5-coder:7b` - Excellent code generation
- `qwen2.5-math:1.5b` - Math problem solving

### Quality Setup (Best Results)
When quality matters most:
- `qwen2.5:7b` - Superior chat quality
- `qwen2.5-coder:32b` - Production-grade code
- `qwen2.5-math:7b` - Advanced mathematics
- `qwenvl2:7b` - Multimodal tasks

## Using the Model Manager

### Basic Usage

```python
from think_ai.models.language.model_manager import ModelManager, TaskType

# Initialize manager
manager = ModelManager({
    "ollama": {"enabled": True},
    "huggingface": {"enabled": True}
})

await manager.initialize()

# Generate with automatic model selection
response, selection = await manager.generate(
    task_type=TaskType.CODING,
    prompt="Write a binary search function",
    prefer_fast=True  # Use smaller/faster model
)

print(f"Used model: {selection.model}")
print(f"Response: {response.text}")
```

### Task-Specific Generation

```python
# Fast chat response
response, _ = await manager.generate(
    TaskType.CHAT,
    "Tell me a joke",
    prefer_fast=True
)

# High-quality code generation
response, _ = await manager.generate(
    TaskType.CODING,
    "Implement a red-black tree",
    prefer_quality=True
)

# Math problem solving
response, _ = await manager.generate(
    TaskType.MATH,
    "Solve the integral of x^2 * e^x"
)
```

## Configuration

### Environment Variables

```bash
# Model provider settings
export OLLAMA_BASE_URL="http://localhost:11434"
export MODEL_PROVIDER_PREFERENCE="ollama,huggingface"

# Default models for tasks
export CHAT_MODEL="qwen2.5:1.5b"
export CODING_MODEL="qwen2.5-coder:1.5b"
export MATH_MODEL="qwen2.5-math:1.5b"
```

### Configuration File

See `config/qwen_models.yaml` for detailed configuration options.

## Performance Characteristics

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| qwen2.5:0.5b | 0.5B | ⚡⚡⚡ | ⭐ | Quick responses, simple queries |
| qwen2.5:1.5b | 1.5B | ⚡⚡ | ⭐⭐ | General chat, basic tasks |
| qwen2.5:3b | 3B | ⚡ | ⭐⭐⭐ | Balanced performance |
| qwen2.5:7b | 7B | 🐌 | ⭐⭐⭐⭐ | High-quality responses |
| qwen2.5-coder:1.5b | 1.5B | ⚡⚡ | ⭐⭐ | Basic code generation |
| qwen2.5-coder:7b | 7B | 🐌 | ⭐⭐⭐⭐ | Complex code tasks |

## Resource Requirements

### Minimal Models (0.5B - 1.5B)
- RAM: 1-2 GB
- CPU: Any modern CPU
- Response time: <1 second

### Medium Models (3B - 7B)  
- RAM: 4-8 GB
- CPU: Recent CPU recommended
- Response time: 2-5 seconds

### Large Models (14B - 32B)
- RAM: 16-32 GB
- CPU: High-end CPU or GPU
- Response time: 5-15 seconds

## Troubleshooting

### Ollama Not Running
```bash
# Check status
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Pull specific model
ollama pull qwen2.5:1.5b
```

### Slow Performance
1. Use smaller models (0.5b or 1.5b)
2. Enable quantization in config
3. Ensure sufficient RAM available
4. Close other applications

## Advanced Usage

### Custom Model Selection

```python
# Override automatic selection
config = GenerationConfig(temperature=0.7)
response = await manager.providers['ollama'].generate(
    model="qwen2.5:0.5b",
    prompt="Hello!",
    config=config
)
```

### Pre-loading Models

```python
# Pre-load frequently used models
await manager.providers['ollama'].load_model("qwen2.5:1.5b")
await manager.providers['ollama'].load_model("qwen2.5-coder:1.5b")
```

### Streaming Responses

```python
async for chunk in manager.providers['ollama'].stream_generate(
    model="qwen2.5:1.5b",
    prompt="Tell me a story",
    config=GenerationConfig()
):
    print(chunk, end='', flush=True)
```

## Best Practices

1. **Start Small**: Begin with 0.5B or 1.5B models
2. **Task Matching**: Use specialized models (coder, math) for specific tasks
3. **Resource Awareness**: Monitor RAM usage with larger models
4. **Fallback Strategy**: Configure both Ollama and HuggingFace providers
5. **Caching**: Enable response caching for repeated queries

## Integration with Think AI Features

The Qwen models integrate seamlessly with:
- O(1) vector search for context retrieval
- Constitutional AI for ethical responses
- Response caching for performance
- Multi-provider failover
- Task-specific optimization

For more details, see the main Think AI documentation.