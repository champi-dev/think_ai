# Quick Start Tutorial

[← Installation](./installation.md) | [Home](../index.md) | [Core Concepts →](./concepts.md)

> **Feynman Explanation**: Using Think AI is like having a conversation with a very smart friend who remembers everything and loves to help!

## 🎯 What You'll Learn

In the next 5 minutes, you'll:
1. Have your first AI conversation
2. Teach your AI something new
3. Use AI to solve a real problem
4. Understand the basics

## 🗣️ Your First Conversation

### Python Example

```python
from think_ai import ThinkAI

# Create your AI assistant (like turning on a smart device)
ai = ThinkAI()

# Say hello! (The AI will respond like a helpful friend)
response = ai.chat("Hello! What's your name and what can you do?")
print(response)
```

**What happens**: The AI introduces itself and explains its capabilities.

### JavaScript Example

```javascript
import { ThinkAI } from 'think-ai-js';

// Create your AI assistant
const ai = new ThinkAI({
  apiUrl: 'http://localhost:8000'  // Where your AI lives
});

// Have a conversation
async function chat() {
  const response = await ai.chat("Hello! What's your name and what can you do?");
  console.log(response);
}

chat();
```

### Command Line Example

```bash
# The simplest way - just type!
think-ai chat "Hello! What's your name and what can you do?"
```

## 🧠 Teaching Your AI

Think AI can learn from you! Here's how to teach it:

### Example: Teaching About Your Favorite Topic

```python
# Teach the AI about something you love
ai.train(
    topic="coffee brewing",
    knowledge="""
    The perfect cup of coffee requires:
    - Water temperature: 195-205°F (90-96°C)
    - Coffee-to-water ratio: 1:15 to 1:17
    - Brew time: 4-5 minutes for pour-over
    - Fresh beans: Use within 2 weeks of roasting
    """,
    iterations=10  # How many times to study this
)

# Now ask about what you taught
response = ai.chat("How do I make the perfect cup of coffee?")
print(response)
```

**What happens**: The AI studies your information and can now give advice about coffee!

## 💡 Solving Real Problems

### Example 1: Writing Helper

```python
# Get help writing an email
response = ai.chat("""
Help me write a friendly email to decline a meeting invitation.
I'm busy with a project deadline.
""")
print(response)
```

### Example 2: Code Assistant

```python
# Get coding help
response = ai.chat("""
Write a Python function that checks if a word is a palindrome.
Explain how it works step by step.
""")
print(response)
```

### Example 3: Learning Partner

```python
# Use Feynman Technique to learn
response = ai.chat("""
Explain quantum computing like I'm 10 years old.
Use simple analogies and examples.
""")
print(response)
```

## 🚀 Interactive Session

Here's a complete interactive session you can run:

```python
from think_ai import ThinkAI

def interactive_session():
    """A fun interactive session with Think AI"""
    
    ai = ThinkAI()
    print("🤖 Think AI is ready! Type 'quit' to exit.\n")
    
    # Conversation loop
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("AI: Goodbye! It was nice talking with you! 👋")
            break
        
        # Get AI response
        response = ai.chat(user_input)
        print(f"AI: {response}\n")

# Run the session
if __name__ == "__main__":
    interactive_session()
```

## 📊 Understanding Responses

Think AI responses have special features:

### Rich Responses
```python
# Ask for structured information
response = ai.chat("List 3 benefits of exercise with explanations")

# The AI provides:
# 1. Clear formatting
# 2. Detailed explanations
# 3. Practical examples
```

### Contextual Memory
```python
# First message
ai.chat("My name is Alice and I love astronomy")

# Later message (AI remembers!)
response = ai.chat("What's my favorite subject?")
# AI responds: "Based on our conversation, your favorite subject is astronomy!"
```

## 🛠️ Basic Configuration

### Setting Preferences

```python
# Create AI with custom settings
ai = ThinkAI(
    model="gpt-3.5-turbo",      # Choose AI model
    temperature=0.7,             # Creativity level (0=focused, 1=creative)
    max_tokens=500,              # Response length limit
    personality="friendly tutor" # AI's personality
)
```

### Understanding Settings

- **Model**: Like choosing between different AI "brains"
- **Temperature**: How creative vs. focused the AI should be
  - 0.1 = Very focused, consistent
  - 0.7 = Balanced (default)
  - 1.0 = Very creative, varied
- **Max Tokens**: Maximum response length (1 token ≈ 4 characters)
- **Personality**: How the AI should behave

## 🎮 Fun Exercises

### Exercise 1: Story Creator
```python
# Create a collaborative story
story = ai.chat("Start a mystery story in 3 sentences")
print(story)

# Continue the story
continuation = ai.chat("Continue the story with a plot twist")
print(continuation)
```

### Exercise 2: Learning Assistant
```python
# Learn something new
topic = "photosynthesis"
explanation = ai.chat(f"Teach me about {topic} using the Feynman technique")
print(explanation)

# Test understanding
quiz = ai.chat(f"Give me a simple quiz about {topic}")
print(quiz)
```

### Exercise 3: Problem Solver
```python
# Solve a real problem
problem = """
I have 3 meetings tomorrow, need to buy groceries, 
and finish a report. How should I organize my day?
"""
solution = ai.chat(problem)
print(solution)
```

## 📈 Next Steps

Now that you've mastered the basics:

### 1. **Dive Deeper**
   - [Core Concepts](./concepts.md) - Understand how Think AI works
   - [Basic Usage Guide](../guides/basic-usage.md) - More examples

### 2. **Advanced Features**
   - [Self-Training Guide](../guides/self-training.md) - Make AI smarter
   - [Advanced Features](../guides/advanced-features.md) - Power user tips

### 3. **Build Something**
   - [Build a Chatbot](../tutorials/chatbot.md) - Create your own assistant
   - [Code Generation](../tutorials/code-generation.md) - AI that codes

## 🆘 Quick Help

### Common Questions

**Q: How do I make responses shorter/longer?**
```python
ai = ThinkAI(max_tokens=100)  # Shorter responses
ai = ThinkAI(max_tokens=1000) # Longer responses
```

**Q: How do I save conversations?**
```python
# Save conversation history
history = ai.get_conversation_history()
with open('conversation.json', 'w') as f:
    json.dump(history, f)
```

**Q: Can I use different languages?**
```python
response = ai.chat("Hola! ¿Cómo estás?")  # Spanish
response = ai.chat("Bonjour!")            # French
# Think AI understands many languages!
```

## 🎉 Congratulations!

You've completed the quick start! You can now:
- ✅ Have conversations with Think AI
- ✅ Teach it new information
- ✅ Solve real problems
- ✅ Configure basic settings

### What's Next?
→ [Learn Core Concepts](./concepts.md) to understand the magic behind Think AI!

---

[← Installation](./installation.md) | [Home](../index.md) | [Core Concepts →](./concepts.md)

**Need help?** Check the [FAQ](../guides/faq.md) or [ask the community](https://github.com/champi-dev/think_ai/discussions) 💬