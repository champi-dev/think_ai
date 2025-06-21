# Basic Usage Guide

[← Core Concepts](../getting-started/concepts.md) | [Home](../index.md) | [Advanced Features →](./advanced-features.md)

> **Feynman Explanation**: Using Think AI is like having a conversation with a helpful assistant who remembers everything and gets smarter over time!

## 📋 Table of Contents
- [Starting Conversations](#starting-conversations)
- [Common Use Cases](#common-use-cases)
- [Working with Context](#working-with-context)
- [Saving and Loading Sessions](#saving-and-loading-sessions)
- [Basic Configuration](#basic-configuration)
- [Tips and Tricks](#tips-and-tricks)

## 💬 Starting Conversations

### The Basics

Think AI conversations work just like talking to a friend:

```python
from think_ai import ThinkAI

# Start your AI
ai = ThinkAI()

# Simple conversation
response = ai.chat("Hello! How are you today?")
print(response)
```

### Different Ways to Chat

#### 1. **Single Questions**
```python
# Quick questions, quick answers
answer = ai.chat("What's the capital of France?")
# "The capital of France is Paris."
```

#### 2. **Multi-turn Conversations**
```python
# AI remembers context
ai.chat("I'm planning a trip to Paris")
ai.chat("What should I see?")  # AI knows you mean Paris
ai.chat("How many days do I need?")  # Still talking about Paris trip
```

#### 3. **Complex Queries**
```python
# Ask complicated questions
response = ai.chat("""
I have $5000 budget and 10 days vacation.
I enjoy history, art, and good food.
Should I visit Paris or Rome?
""")
# AI provides detailed comparison and recommendation
```

## 🎯 Common Use Cases

### 1. Personal Assistant

```python
# Daily planning
ai.chat("I have 3 meetings today, gym at 6pm, and need to buy groceries. Help me plan my day")

# Reminders
ai.remember("task", "Call dentist for appointment")
ai.chat("What did I need to do today?")

# Decision making
ai.chat("Should I buy a laptop now or wait for Black Friday? I need it for programming")
```

### 2. Learning Companion

```python
# Learn new topics
ai.chat("Explain machine learning like I'm a beginner")

# Practice problems
ai.chat("Give me 5 Python coding exercises for beginners")

# Study help
ai.chat("Quiz me on World War 2 history")
```

### 3. Creative Partner

```python
# Writing help
ai.chat("Help me write an email declining a job offer politely")

# Brainstorming
ai.chat("I need creative names for a coffee shop in Seattle")

# Storytelling
ai.chat("Continue this story: The door creaked open, revealing...")
```

### 4. Problem Solver

```python
# Technical issues
ai.chat("My Python code gives 'IndexError'. Here's the code: [paste code]")

# Life advice
ai.chat("I'm nervous about my job interview tomorrow. Any tips?")

# Analysis
ai.chat("Analyze pros and cons of electric vs hybrid cars for city driving")
```

## 🧩 Working with Context

### Understanding Context

Think AI remembers your conversation like a human would:

```python
# Set context at the start
ai.chat("I'm a web developer working on an e-commerce site")

# All future questions are understood in this context
ai.chat("What database should I use?")  # AI knows you mean for e-commerce
ai.chat("How do I handle payments?")     # Still about your e-commerce site
```

### Managing Context

#### Clear Context
```python
# Start fresh
ai.clear_context()
ai.chat("Let's talk about something new")
```

#### Set Specific Context
```python
# Provide background information
ai.set_context({
    "user_role": "student",
    "subject": "biology",
    "level": "high school"
})

ai.chat("Explain photosynthesis")  # Gets high-school level explanation
```

#### Context Windows
```python
# Check how much context AI is tracking
context_info = ai.get_context_info()
print(f"Messages in context: {context_info['message_count']}")
print(f"Context size: {context_info['token_count']} tokens")
```

## 💾 Saving and Loading Sessions

### Save Your Conversations

```python
# After a useful conversation
conversation = ai.get_conversation_history()

# Save to file
import json
with open('my_ai_session.json', 'w') as f:
    json.dump(conversation, f, indent=2)
```

### Resume Later

```python
# Load previous conversation
with open('my_ai_session.json', 'r') as f:
    previous_conversation = json.load(f)

# Create new AI with history
ai = ThinkAI()
ai.load_conversation(previous_conversation)

# Continue where you left off
ai.chat("What were we discussing?")
```

### Export Formats

```python
# Export as markdown (great for notes)
ai.export_conversation('conversation.md', format='markdown')

# Export as PDF (for documentation)
ai.export_conversation('conversation.pdf', format='pdf')

# Export as plain text
ai.export_conversation('conversation.txt', format='text')
```

## ⚙️ Basic Configuration

### Adjusting AI Behavior

```python
# Create AI with custom settings
ai = ThinkAI(
    # How creative vs focused (0.0 - 1.0)
    temperature=0.7,  
    
    # Maximum response length
    max_tokens=500,
    
    # Response style
    style="friendly",
    
    # Expertise level
    expertise="intermediate"
)
```

### Common Configurations

#### For Precise Work (coding, math)
```python
ai = ThinkAI(
    temperature=0.2,  # Very focused
    style="technical",
    format="structured"
)
```

#### For Creative Work (writing, brainstorming)
```python
ai = ThinkAI(
    temperature=0.8,  # More creative
    style="creative",
    format="conversational"
)
```

#### For Learning (studying, tutorials)
```python
ai = ThinkAI(
    temperature=0.5,  # Balanced
    style="educational",
    expertise="beginner"
)
```

### Response Formats

```python
# Get structured responses
ai.set_format("json")
response = ai.chat("List 3 benefits of exercise")
# Returns: {"benefits": ["improves health", "boosts mood", "increases energy"]}

# Get markdown formatted
ai.set_format("markdown")
response = ai.chat("Explain Python functions")
# Returns formatted with headers, code blocks, lists

# Get plain text
ai.set_format("text")
response = ai.chat("Tell me about dogs")
# Returns simple plain text
```

## 💡 Tips and Tricks

### 1. **Be Specific**
```python
# ❌ Vague
ai.chat("Help me with code")

# ✅ Specific
ai.chat("Help me fix this Python TypeError in my Django view function")
```

### 2. **Provide Examples**
```python
# Give examples for better results
ai.chat("""
Format this data like:
Name: John Doe
Age: 30
City: New York

Here's my data: john smith 25 los angeles
""")
```

### 3. **Use Follow-ups**
```python
# Don't accept the first answer if you need more
response = ai.chat("How do I cook pasta?")
followup = ai.chat("Can you be more specific about the timing?")
details = ai.chat("What about for different pasta types?")
```

### 4. **Correct Mistakes**
```python
# AI learns from corrections
ai.chat("The capital of Australia is Sydney")
ai.chat("Actually, it's Canberra. Please remember that.")
# AI updates its understanding
```

### 5. **Use Templates**
```python
# Create reusable templates
email_template = """
Write a professional email with:
- Recipient: {recipient}
- Purpose: {purpose}
- Tone: {tone}
- Key points: {points}
"""

response = ai.chat(email_template.format(
    recipient="my manager",
    purpose="request time off",
    tone="polite but confident",
    points="need Dec 20-25 off for family vacation"
))
```

## 🎮 Interactive Examples

### Example 1: Daily Journal

```python
# Create a journaling assistant
def daily_journal():
    ai = ThinkAI(style="supportive")
    
    # Check in
    ai.chat("Let's reflect on your day. How was it overall?")
    
    # Guide reflection
    prompts = [
        "What went well today?",
        "What was challenging?",
        "What did you learn?",
        "What are you grateful for?"
    ]
    
    for prompt in prompts:
        response = input(f"AI: {prompt}\nYou: ")
        ai.chat(f"I said: {response}")
    
    # Summary
    summary = ai.chat("Summarize my reflections and suggest one area for tomorrow's focus")
    print(f"AI: {summary}")
```

### Example 2: Recipe Assistant

```python
# Interactive cooking helper
def recipe_assistant():
    ai = ThinkAI()
    
    # Get preferences
    ingredients = input("What ingredients do you have? ")
    dietary = input("Any dietary restrictions? ")
    time = input("How much time do you have? ")
    
    # Get recipe
    recipe = ai.chat(f"""
    Create a recipe using: {ingredients}
    Dietary restrictions: {dietary}
    Time available: {time}
    Format with clear steps and timing.
    """)
    
    print(recipe)
    
    # Interactive cooking
    while True:
        question = input("Any questions while cooking? (or 'done'): ")
        if question.lower() == 'done':
            break
        answer = ai.chat(question)
        print(f"AI: {answer}")
```

### Example 3: Language Practice

```python
# Language learning buddy
def language_practice(language="Spanish"):
    ai = ThinkAI()
    
    ai.chat(f"Let's practice {language}. I'll be your conversation partner.")
    
    # Practice scenarios
    scenarios = [
        "ordering at a restaurant",
        "asking for directions",
        "shopping at a market",
        "making small talk"
    ]
    
    for scenario in scenarios:
        print(f"\n--- Practicing: {scenario} ---")
        
        # AI starts
        ai_start = ai.chat(f"Start a {language} conversation about {scenario}")
        print(f"AI: {ai_start}")
        
        # Practice conversation
        for _ in range(3):
            your_response = input("You: ")
            ai_response = ai.chat(f"Continue in {language}: {your_response}")
            print(f"AI: {ai_response}")
        
        # Get feedback
        feedback = ai.chat("How did I do? Give feedback on my language use")
        print(f"Feedback: {feedback}")
```

## 📊 Monitoring Usage

### Track Your AI Usage

```python
# Get usage statistics
stats = ai.get_usage_stats()

print(f"Total messages: {stats['total_messages']}")
print(f"Total tokens used: {stats['total_tokens']}")
print(f"Average response time: {stats['avg_response_time']}ms")
print(f"Session duration: {stats['session_duration']} minutes")
```

### Set Usage Limits

```python
# Prevent excessive usage
ai.set_limits(
    max_messages_per_hour=100,
    max_tokens_per_day=50000,
    max_response_length=1000
)

# Get notified when approaching limits
ai.on_limit_warning(lambda: print("Approaching usage limit!"))
```

## 🚀 Next Steps

You're now ready for more advanced features:

### Explore:
- [Advanced Features](./advanced-features.md) - Power user capabilities
- [Self-Training Guide](./self-training.md) - Make your AI smarter
- [API Reference](./api-reference.md) - Detailed documentation

### Build:
- [Create a Chatbot](../tutorials/chatbot.md) - Build your own assistant
- [Code Generation](../tutorials/code-generation.md) - AI that writes code
- [Real Examples](../tutorials/examples.md) - See what others built

---

[← Core Concepts](../getting-started/concepts.md) | [Home](../index.md) | [Advanced Features →](./advanced-features.md)

**Need help?** Join our [community](https://github.com/champi-dev/think_ai/discussions) 💬