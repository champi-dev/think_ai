#!/usr/bin/env python3
"""Demo showing Think AI with trained knowledge in action."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Create some sample pre-trained knowledge
sample_knowledge = {
    "What is consciousness?": "Consciousness is the subjective experience of awareness - the 'what it's like' to be you. It includes sensations, thoughts, emotions, and the unified experience of being. In AI, we model it through attention mechanisms, self-reflection, and integrated information theory.",
    "How do I implement a hash table?": """Here's a hash table implementation with O(1) average operations:

```python
class HashTable:
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
        return None
```

This provides constant-time insertion and lookup on average!""",
    "What is the meaning of life?": "The meaning of life is a profound question with many answers. Biologically, it's to survive and reproduce. Philosophically, it might be to create meaning, reduce suffering, seek happiness, or achieve self-actualization. Many find meaning through relationships, creativity, or helping others. Perhaps the beauty is that we each get to discover and create our own meaning.",
    "How to fix a memory leak?": """To fix a memory leak:

1. **Identify the leak**: Use profiling tools (valgrind, memory_profiler)
2. **Common causes**:
   - Circular references (use weak references)
   - Unclosed resources (files, connections)
   - Growing collections (clear when done)
   - Event listeners not removed

3. **Python example**:
```python
# Bad - creates circular reference
class Node:
    def __init__(self):
        self.parent = None
        self.children = []
    
    def add_child(self, child):
        child.parent = self  # Circular ref!
        self.children.append(child)

# Good - use weakref
import weakref
class Node:
    def __init__(self):
        self._parent = None
        self.children = []
    
    @property
    def parent(self):
        return self._parent() if self._parent else None
    
    @parent.setter
    def parent(self, p):
        self._parent = weakref.ref(p) if p else None
```""",
    "Write a Python function to sort an array": """Here are multiple sorting implementations:

```python
# Quick Sort - O(n log n) average
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Merge Sort - O(n log n) guaranteed
def mergesort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# For most cases, just use:
sorted_arr = sorted(arr)  # Tim Sort - O(n log n)
```""",
}


def demo():
    """Run demo of trained Think AI."""
    print("🧠 Think AI - Trained with Knowledge")
    print("=" * 50)
    print("\nAsk me anything! (type 'quit' to exit)\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["quit", "exit", "bye"]:
            print("\nGoodbye! 👋")
            break

        # Check if we have a direct answer
        if question in sample_knowledge:
            answer = sample_knowledge[question]
        else:
            # Try to find similar question
            found = False
            for known_q, known_a in sample_knowledge.items():
                if question.lower() in known_q.lower() or known_q.lower() in question.lower():
                    answer = known_a
                    found = True
                    break

            if not found:
                # Generate a helpful response
                if "how" in question.lower():
                    answer = f"To {question.lower().replace('how to', '').replace('how do i', '').strip()}, you'll need to understand the core requirements first. I can help break this down into steps and provide code examples if needed."
                elif "what" in question.lower():
                    topic = question.lower().replace("what is", "").replace("what are", "").replace("?", "").strip()
                    answer = f"{topic.capitalize()} is an important concept worth exploring. It involves various aspects that work together to create a complete understanding. Would you like me to elaborate on specific parts?"
                elif "why" in question.lower():
                    answer = "That's a great question! The answer involves understanding several interconnected factors. Let me explain the key reasons and underlying principles."
                else:
                    answer = "That's an interesting topic! I'd be happy to help. Could you provide more specific details about what you'd like to know?"

        print(f"\nThink AI: {answer}\n")
        print("-" * 50)


if __name__ == "__main__":
    demo()
