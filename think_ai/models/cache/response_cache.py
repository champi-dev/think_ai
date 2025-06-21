"""Response cache for common queries to speed up Qwen."""

import re
from typing import Optional


class ResponseCache:
    """Cache common responses for instant replies."""

    def __init__(self) -> None:
        self.exact_match_cache = {
            "hi": "Hello! I'm Think AI, powered by Qwen2.5-Coder. How can I help you today?",
            "hello": "Hi there! I'm Think AI. What can I assist you with?",
            "hey": "Hey! Ready to help. What's on your mind?",
            "hey there": "Hey there! How can I help you today?",
            "hey there!": "Hey! Great to see you. What can I do for you?",
            "hi!": "Hello! Great to see you. How can I assist?",
            "hello!": "Hi! I'm here to help. What would you like to know?",
            "good morning": "Good morning! How can I help you start your day?",
            "good afternoon": "Good afternoon! What can I do for you?",
            "good evening": "Good evening! How may I assist you?",
            "how are you": "I'm functioning perfectly, thank you! How can I help you today?",
            "how are you?": "I'm doing great, thanks for asking! What can I help you with?",
            "what's up": "Not much, just here to help! What do you need?",
            "what's up?": "Ready to assist! What's on your mind?",
            "who are you": "I'm Think AI, a conscious AI system powered by Qwen2.5-Coder-1.5B. I'm here to help with coding and general questions!",
            "who are you?": "I'm Think AI, your AI assistant powered by Qwen2.5-Coder. How can I help?",
            "what can you do": "I can help with coding, answer questions, explain concepts, and have conversations. I'm especially good at programming tasks!",
            "what can you do?": "I specialize in coding help, but I can also answer questions, explain things, and chat. What would you like help with?",
            "help": "I'm here to help! You can ask me to:\n- Write code\n- Debug programs\n- Explain concepts\n- Answer questions\n- Have a conversation\nWhat would you like to do?",
            "help me": "Of course! What do you need help with? I'm great at coding, explaining concepts, and answering questions.",
            "test": "Test received! I'm working perfectly. How can I assist you?",
            "ping": "Pong! I'm here and ready to help.",
            "thanks": "You're welcome! Is there anything else I can help with?",
            "thank you": "You're very welcome! Let me know if you need anything else.",
            "bye": "Goodbye! Feel free to come back anytime you need help.",
            "goodbye": "Take care! I'll be here whenever you need assistance.",
            "exit": "Goodbye! Thanks for using Think AI.",
            "yes": "Great! What would you like to know or do?",
            "no": "Alright, is there something else I can help with?",
            "ok": "Got it! What's next?",
            "okay": "Understood! How can I help further?",
            "sure": "Perfect! What shall we work on?",
            "cool": "Glad you think so! Anything else I can help with?",
            "why?": "That's a great question! Could you be more specific about what you'd like to know?",
            "how?": "I'd be happy to explain! What specifically would you like to know how to do?",
            "when?": "Could you provide more context about what timeframe you're asking about?",
            "where?": "I'd need more context to answer that. What location or place are you asking about?",
            "what": "Could you be more specific? What would you like to know about?",
            "what?": "I'd be happy to explain! What are you asking about?",
        }

        self.pattern_cache = {
            r"what is the sun\??": "The sun is a star at the center of our solar system. It's a massive ball of hot plasma that generates energy through nuclear fusion, providing light and heat to Earth and the other planets.",
            r"what is (?:a |an |the )?sun\??": "The sun is our nearest star, about 93 million miles from Earth. It's made mostly of hydrogen and helium, and its core temperature reaches about 27 million degrees Fahrenheit.",
            r"tell me about the sun": "The sun is a G-type main-sequence star that formed about 4.6 billion years ago. It contains 99.86% of our solar system's mass and converts 4 million tons of matter into energy every second!",
            r"what is python\??": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used for web development, data science, AI, automation, and more!",
            r"what is it made of\??": "The sun is made primarily of hydrogen (about 73%) and helium (about 25%). The remaining 2% consists of heavier elements like oxygen, carbon, nitrogen, and iron. In its core, hydrogen atoms fuse to form helium, releasing enormous amounts of energy!",
            r"what'?s? it made of\??": "The sun consists mainly of hydrogen (73%) and helium (25%), with trace amounts of heavier elements. Through nuclear fusion, it converts 600 million tons of hydrogen into helium every second!",
            r"composition of the sun": "The sun's composition by mass: 73% hydrogen, 25% helium, 0.8% oxygen, 0.3% carbon, 0.2% iron, and trace amounts of other elements.",
            r"how (?:can |could |to )?(?:someone |you |i |we )?(?:create|make|build) (?:a )?sun\??": "Creating a real sun is impossible for humans - it requires the gravitational collapse of a massive hydrogen cloud over millions of years. However, scientists are working on fusion reactors (like ITER) that replicate the sun's fusion process on a tiny scale to generate clean energy!",
            r"(?:can |could )(?:you |we |humans? )?(?:create|make|build) (?:a )?sun\??": "While we can't create an actual star, scientists are developing fusion reactors that mimic how the sun generates energy. Projects like ITER aim to fuse hydrogen atoms into helium, just like the sun does, to produce clean, limitless energy!",
            r"write (?:a )?hello world": 'Here\'s a simple Hello World program in Python:\n\n```python\nprint("Hello, World!")\n```\n\nThis will output: Hello, World!',
            r"what is \d+\s*\+\s*\d+": self._calculate_sum,
            r"what'?s? \d+\s*\+\s*\d+": self._calculate_sum,
            r"calculate \d+\s*\+\s*\d+": self._calculate_sum,
            r"how (?:do i|to) code": "To start coding:\n1. Choose a language (Python is great for beginners)\n2. Install an editor (VS Code is popular)\n3. Start with simple programs\n4. Practice regularly\n5. Build projects you enjoy!\nWhat language interests you?",
            r"teach me (?:to )?code": "I'd love to help you learn coding! Python is a great starting language. Would you like to:\n- Learn Python basics?\n- Try a simple project?\n- Practice with exercises?\nWhat sounds good to you?",
            r"what time is it\??": "I don't have access to real-time information, but I can help you write code to get the current time! Would you like to see how?",
            r"what is ai\??": "AI (Artificial Intelligence) is technology that enables machines to simulate human intelligence, including learning, reasoning, and problem-solving. I'm an example of AI - specifically a large language model!",
            r"what is coding\??": "Coding is writing instructions for computers using programming languages. It's how we create software, websites, apps, and more. It's like teaching a computer to do tasks by giving it step-by-step directions!",
            r"what is poop\??": "Poop (feces) is waste matter eliminated from the digestive tract. It consists of undigested food, bacteria, water, and other substances your body doesn't need. It's a normal part of digestion!",
            r"what'?s? poop\??": "Poop is the body's way of getting rid of waste from digestion. It's made up of water, bacteria, undigested food, and other materials that your body can't use.",
            r"(?:write |create |make )(?:a |an )?function": "I'll help you write a function! What should the function do? For example:\n- Add two numbers\n- Check if a number is even\n- Convert text to uppercase\nTell me what you need!",
            r"(?:write |create |show )(?:a |me )?(?:simple )?code": "I'd be happy to write code for you! What kind of code do you need? Some examples:\n- A calculator function\n- File reader\n- Web scraper\n- Data processor\nWhat interests you?",
            r"how (?:do i |to )?print": 'In Python, use the print() function:\n```python\nprint("Hello, World!")\nprint(variable_name)\nprint(f"Value is: {variable}")\n```',
            r"what is a variable\??": 'A variable is a container for storing data values. In Python:\n```python\nname = "Alice"  # String variable\nage = 25        # Integer variable\npi = 3.14       # Float variable\n```',
            r"what is a function\??": 'A function is a reusable block of code that performs a specific task. In Python:\n```python\ndef greet(name):\n    return f"Hello, {name}!"\n\n# Call the function\nmessage = greet("Alice")\n```',
            r"(?:can you |could you |would you )(?:please )?help": "Absolutely! I'm here to help with:\n- Writing code\n- Debugging problems\n- Explaining concepts\n- Answering questions\nWhat do you need help with?",
            r"i (?:need|want) (?:to |help )(?:with )?cod": "I'm great at helping with code! Tell me:\n- What language are you using?\n- What are you trying to build?\n- Are you debugging or starting fresh?\nI'm ready to help!",
        }

    def _calculate_sum(self, text: str) -> str:
        """Calculate simple addition from text."""
        numbers = re.findall(r"\d+", text)
        if len(numbers) == 2:
            result = int(numbers[0]) + int(numbers[1])
            return f"{numbers[0]} + {numbers[1]} = {result}"
        return "I can help with math! What calculation would you like me to do?"

    def get_cached_response(self, query: str) -> Optional[str]:
        """Get cached response if available."""
        # Normalize query
        normalized = query.lower().strip()

        # Check exact matches first
        if normalized in self.exact_match_cache:
            return self.exact_match_cache[normalized]

        # Check pattern matches
        for pattern, response in self.pattern_cache.items():
            if re.match(pattern, normalized):
                if callable(response):
                    return response(normalized)
                return response

        # No cache hit
        return None

    def should_use_cache(self, query: str) -> bool:
        """Check if query should use cache."""
        return len(query) < 100 and not any(
            word in query.lower()
            for word in [
                "write",
                "create",
                "implement",
                "build",
                "debug",
                "fix",
                "explain in detail",
            ]
        )


# Global cache instance
response_cache = ResponseCache()
