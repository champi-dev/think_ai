# Think AI Coding CLI - Mode Switching Guide

## How to Switch Between CODE and CHAT Modes

The Think AI Coding CLI now supports two distinct modes:

### 🚀 CODE Mode (Default)
- Generates actual code based on your descriptions
- Examples:
  - `hello` → Generates "Hello, World!" code
  - `fibonacci` → Generates Fibonacci implementation
  - `crud postgresql` → Generates database CRUD operations

### 💬 CHAT Mode
- Answers questions and has conversations
- Examples:
  - `hello` → Responds with a greeting
  - `what is the sun?` → Explains what the sun is
  - `how are you?` → Has a friendly conversation

## Mode Switching

Simply type `mode` to toggle between modes:

```bash
think-ai-coding (python | CODE)> mode
🔄 Switched to CHAT mode
think-ai-coding (python | CHAT)> what is the sun?
The sun is a star at the center of our solar system...
```

## Visual Indicators

The prompt shows your current mode:
- `think-ai-coding (python | CODE)>` - You're in CODE generation mode
- `think-ai-coding (python | CHAT)>` - You're in CHAT conversation mode

## Quick Start

```bash
# Run the coding CLI
./target/release/think-ai-coding chat

# Inside the CLI:
# Type 'mode' to switch modes
# Type 'help' to see all commands
# Type 'exit' to quit
```

## Examples

### CODE Mode Example:
```
think-ai-coding (python | CODE)> fibonacci
⚡ Generated from pattern in 1.234ms

```python
def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number efficiently"""
    if n <= 1:
        return n
    # ... full implementation
```

### CHAT Mode Example:
```
think-ai-coding (python | CHAT)> what is the sun?

The sun is a star at the center of our solar system. It's a nearly perfect sphere of hot plasma...
```

Enjoy coding and chatting with Think AI! 🎉