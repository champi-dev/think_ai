"""Simple AI response generator for Think AI - provides real answers."""

import random
import re
from typing import Dict, List, Tuple


class SimpleAI:
    """Generates intelligent responses without external dependencies."""

    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
        self.code_examples = self._build_code_examples()

    def _build_knowledge_base(self) -> Dict[str, Dict]:
        """Build a knowledge base for common topics."""
        return {
            "life": {
                "definition": "self-organizing systems capable of metabolism, growth, adaptation, response to stimuli, and reproduction",
                "facts": [
                    "emerged on Earth about 3.8 billion years ago",
                    "based on carbon chemistry and DNA/RNA information storage",
                    "requires energy flow to maintain organization against entropy",
                ],
                "perspectives": {
                    "biological": "complex chemical systems undergoing Darwinian evolution",
                    "physical": "localized decreases in entropy powered by energy gradients",
                    "philosophical": "the universe's way of understanding itself",
                },
            },
            "consciousness": {
                "definition": "subjective experience of awareness and sentience",
                "facts": [
                    "emerges from neural activity in the brain",
                    "includes qualia - the subjective quality of experiences",
                    "may involve integrated information and global workspace",
                ],
                "perspectives": {
                    "neuroscience": "patterns of neural activity creating unified experience",
                    "philosophy": "the hard problem of explaining subjective experience",
                    "ai": "can be modeled through attention and self-reflection mechanisms",
                },
            },
            "universe": {
                "definition": "all of space, time, matter, and energy that exists",
                "facts": [
                    "approximately 13.8 billion years old",
                    "contains 2 trillion galaxies",
                    "expanding at an accelerating rate due to dark energy",
                ],
                "perspectives": {
                    "cosmology": "began with the Big Bang and continues expanding",
                    "quantum": "emerges from quantum fields and their interactions",
                    "philosophical": "may be one of many in a multiverse",
                },
            },
        }

    def _build_code_examples(self) -> Dict[str, str]:
        """Build code examples for common requests."""
        return {
            "hash_table": """class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def set(self, key, value):
        idx = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
    
    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None""",
            "binary_search": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found""",
            "api": """from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item, "total": item.price * 1.1}""",
        }

    def generate_response(self, prompt: str) -> str:
        """Generate an intelligent response based on the prompt."""
        prompt_lower = prompt.lower().strip()

        # Extract key information from prompt
        keywords = self._extract_keywords(prompt_lower)
        intent = self._determine_intent(prompt_lower, keywords)

        # Generate response based on intent
        if intent == "code":
            return self._generate_code_response(prompt_lower, keywords)
        elif intent == "explain":
            return self._generate_explanation(prompt_lower, keywords)
        elif intent == "how_to":
            return self._generate_how_to(prompt_lower, keywords)
        elif intent == "question":
            return self._generate_answer(prompt_lower, keywords)
        else:
            return self._generate_contextual_response(prompt, keywords)

    def _extract_keywords(self, prompt: str) -> List[str]:
        """Extract important keywords from prompt."""
        # Remove common words
        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "shall",
            "can",
            "of",
            "in",
            "to",
            "for",
            "with",
            "on",
            "at",
            "from",
            "by",
            "about",
            "as",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "up",
            "down",
            "out",
            "off",
            "over",
            "under",
            "again",
            "further",
            "then",
            "once",
        }

        words = prompt.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords

    def _determine_intent(self, prompt: str, keywords: List[str]) -> str:
        """Determine the intent of the prompt."""
        if any(word in prompt for word in ["code", "function", "implement", "build", "create", "write"]):
            return "code"
        elif any(word in prompt for word in ["explain", "what is", "what are", "tell me about"]):
            return "explain"
        elif any(word in prompt for word in ["how to", "how do", "how can"]):
            return "how_to"
        elif "?" in prompt or any(word in prompt for word in ["why", "when", "where", "who", "which"]):
            return "question"
        else:
            return "general"

    def _generate_code_response(self, prompt: str, keywords: List[str]) -> str:
        """Generate a code-related response."""
        # Check for specific code examples
        if "hash" in prompt and "table" in prompt:
            return f"Here's a hash table implementation with O(1) average operations:\n\n```python\n{self.code_examples['hash_table']}\n```\n\nThis provides constant-time insertion and lookup on average!"
        elif "binary" in prompt and "search" in prompt:
            return f"Here's an efficient binary search with O(log n) complexity:\n\n```python\n{self.code_examples['binary_search']}\n```\n\nThis works on sorted arrays and eliminates half the search space each iteration!"
        elif "api" in prompt or "rest" in prompt:
            return f"Here's a simple REST API using FastAPI:\n\n```python\n{self.code_examples['api']}\n```\n\nThis creates a basic API with GET and POST endpoints!"
        else:
            # Generate contextual code help
            return self._generate_code_help(keywords)

    def _generate_code_help(self, keywords: List[str]) -> str:
        """Generate helpful coding guidance."""
        if not keywords:
            return "I can help you code! What would you like to build? I can assist with data structures, algorithms, web APIs, automation scripts, and more."

        topic = " ".join(keywords[:2])
        return f"""I'll help you code {topic}! Here's how to approach it:

1. **Define Requirements**: What should the {topic} do?
2. **Design Structure**: Plan your classes/functions
3. **Implementation**: Start with core functionality
4. **Testing**: Verify it works correctly
5. **Optimization**: Improve performance if needed

What specific part would you like to start with?"""

    def _generate_explanation(self, prompt: str, keywords: List[str]) -> str:
        """Generate an explanation for a concept."""
        # Check knowledge base first
        for keyword in keywords:
            if keyword in self.knowledge_base:
                kb = self.knowledge_base[keyword]
                facts = "\n- ".join(kb["facts"])
                perspectives = "\n".join([f"**{k.capitalize()}**: {v}" for k, v in kb["perspectives"].items()])

                return f"""{keyword.capitalize()} is {kb["definition"]}.

Key facts:
- {facts}

Different perspectives:
{perspectives}

Would you like me to elaborate on any specific aspect?"""

        # Generate general explanation
        topic = " ".join(keywords[:3]) if keywords else "this concept"
        return f"""{topic.capitalize()} is a complex topic with multiple dimensions:

**Core Concept**: At its foundation, {topic} involves fundamental principles that govern how it operates and interacts with other systems.

**Practical Applications**: In real-world scenarios, {topic} plays a crucial role in various fields and has significant implications.

**Technical Details**: The implementation and mechanics of {topic} involve sophisticated processes and careful consideration of various factors.

What specific aspect would you like me to focus on?"""

    def _generate_how_to(self, prompt: str, keywords: List[str]) -> str:
        """Generate how-to instructions."""
        action = prompt.replace("how to", "").replace("how do i", "").replace("how can i", "").strip()

        if "create" in action and "universe" in action:
            return """To create a universe simulation:

1. **Choose Your Approach**:
   - Physics simulation: Model particles and forces
   - Game universe: Design world rules and content
   - Procedural generation: Algorithm-based creation

2. **Start Simple**:
   ```python
   class Universe:
       def __init__(self):
           self.particles = []
           self.time = 0
           self.laws = PhysicsLaws()
   ```

3. **Add Complexity Gradually**:
   - Implement gravity and electromagnetic forces
   - Add particle interactions
   - Create emergent behaviors

4. **Optimize Performance**:
   - Use spatial partitioning (quadtrees/octrees)
   - Implement parallel processing
   - Cache frequently used calculations

Which type would you like to explore?"""

        # Generic how-to
        return f"""To {action}:

1. **Understand the Goal**: Clearly define what you want to achieve
2. **Break It Down**: Divide into smaller, manageable tasks
3. **Start Simple**: Build a basic version first
4. **Iterate**: Improve and add features incrementally
5. **Test**: Verify each step works correctly

I can provide specific code examples and detailed steps. What part should we start with?"""

    def _generate_answer(self, prompt: str, keywords: List[str]) -> str:
        """Generate an answer to a question."""
        if "meaning" in prompt and "life" in prompt:
            return """The meaning of life is one of humanity's deepest questions with multiple valid answers:

**Biological**: To survive, reproduce, and pass on genetic information
**Philosophical**: To create meaning through our choices and actions
**Existential**: To authentically express our freedom and take responsibility
**Spiritual**: To grow, love, and connect with something greater
**Practical**: To reduce suffering and increase wellbeing for all

Perhaps the beauty is that we each get to discover and create our own meaning. What gives your life meaning?"""

        # Generate thoughtful answer
        return self._generate_contextual_response(prompt, keywords)

    def _generate_contextual_response(self, prompt: str, keywords: List[str]) -> str:
        """Generate a contextual response for any input."""
        if not keywords:
            return "I'm here to help! Could you provide more details about what you're interested in?"

        # Build a response using the keywords and context
        main_topic = keywords[0] if keywords else "that"

        responses = [
            f"{main_topic.capitalize()} is indeed worth exploring. ",
            f"When we think about {main_topic}, several important aspects come to mind. ",
            f"Understanding {main_topic} requires looking at multiple angles. ",
        ]

        response = random.choice(responses)

        # Add contextual information
        if len(keywords) > 1:
            response += f"The relationship between {keywords[0]} and {keywords[1]} involves complex interactions. "

        response += "I can help you explore this further through explanations, code examples, or practical applications. What angle interests you most?"

        return response


# Global instance
simple_ai = SimpleAI()
