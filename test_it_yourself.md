# 🧪 Test Think AI's Proper Architecture Yourself

## 1. Quick Test - See Architecture in Action

```bash
# Run the automated demonstration
python3 demonstrate_proper_architecture.py
```

Watch how:
- First "What is consciousness?" query uses Claude
- Second identical query comes from CACHE (instant, $0 cost!)
- Knowledge base provides facts
- Each component contributes

## 2. Interactive Test - Chat with Think AI

```bash
# Start interactive chat with proper architecture
python3 interactive_proper_chat.py
```

Try these experiments:
- Ask the same question twice (see cache work)
- Ask about topics in knowledge base (consciousness, AI ethics, distributed systems)
- Ask random questions (see when Claude is needed)
- Teach it facts with `/learn <fact>`

## 3. Architecture Comparison Test

```bash
# See old vs new architecture side-by-side
python3 migrate_to_proper_architecture.py
```

This shows:
- Old: Every query → Claude ($$$)
- New: Cache + Knowledge + LLM → Claude only when needed ($)

## 4. Manual Component Testing

### Test ScyllaDB Storage
```python
# In Python REPL
import asyncio
from implement_proper_architecture import ProperThinkAI

async def test_scylla():
    ai = ProperThinkAI()
    await ai.initialize()
    
    # Check stored knowledge
    count = 0
    async for key, item in ai.services['scylla'].scan(prefix="knowledge_", limit=10):
        print(f"Found: {key}")
        count += 1
    print(f"Total knowledge entries: {count}")
    
    await ai.shutdown()

asyncio.run(test_scylla())
```

### Test Cache Effectiveness
```python
async def test_cache():
    ai = ProperThinkAI()
    await ai.initialize()
    
    # First query - will process fully
    print("Query 1 - No cache")
    result1 = await ai.process_with_proper_architecture("What is AI?")
    print(f"Claude used: {result1['architecture_usage']['enhancement']}")
    
    # Same query - should hit cache
    print("\nQuery 2 - Should hit cache")
    result2 = await ai.process_with_proper_architecture("What is AI?")
    print(f"Cache status: {result2['architecture_usage']['cache']}")
    
    await ai.shutdown()

asyncio.run(test_cache())
```

## 5. Cost Tracking Test

```python
async def track_costs():
    ai = ProperThinkAI()
    await ai.initialize()
    
    queries = [
        "What is consciousness?",
        "How does ScyllaDB work?",
        "What is consciousness?",  # Duplicate - cache hit
        "Explain love-based AI",
        "How does ScyllaDB work?"  # Duplicate - cache hit
    ]
    
    for q in queries:
        result = await ai.process_with_proper_architecture(q)
        
    # Check final costs
    costs = ai.claude.get_cost_summary()
    print(f"\nTotal queries: {len(queries)}")
    print(f"Claude API calls: {costs['request_count']}")
    print(f"Cache hits: {len(queries) - costs['request_count']}")
    print(f"Total cost: ${costs['total_cost']:.4f}")
    print(f"Savings: {(1 - costs['request_count']/len(queries))*100:.0f}%")
    
    await ai.shutdown()

asyncio.run(track_costs())
```

## 6. Knowledge Base Test

```bash
# Create a script to add your own knowledge
cat > add_knowledge.py << 'EOF'
import asyncio
from implement_proper_architecture import ProperThinkAI

async def add_custom_knowledge():
    ai = ProperThinkAI()
    await ai.initialize()
    
    # Add your domain knowledge
    my_facts = [
        "Python is the best language for AI development",
        "Think AI was created by a developer who values cost efficiency",
        "ScyllaDB provides O(1) performance at scale"
    ]
    
    for fact in my_facts:
        # Store in knowledge base
        await ai._store_fact(fact)
        print(f"Stored: {fact}")
    
    # Now test retrieval
    result = await ai.process_with_proper_architecture("What language is best for AI?")
    print(f"\nResponse uses your knowledge: {result['response']}")
    
    await ai.shutdown()

asyncio.run(add_custom_knowledge())
EOF

python3 add_knowledge.py
```

## 7. Performance Benchmark

```bash
# Create performance test
cat > benchmark_architecture.py << 'EOF'
import asyncio
import time
from implement_proper_architecture import ProperThinkAI

async def benchmark():
    ai = ProperThinkAI()
    await ai.initialize()
    
    # Test 1: Cold query (no cache)
    start = time.time()
    await ai.process_with_proper_architecture("Explain quantum computing")
    cold_time = time.time() - start
    
    # Test 2: Warm query (cached)
    start = time.time()
    await ai.process_with_proper_architecture("Explain quantum computing")
    warm_time = time.time() - start
    
    print(f"Cold query: {cold_time:.2f}s")
    print(f"Cached query: {warm_time:.2f}s")
    print(f"Speed improvement: {cold_time/warm_time:.1f}x faster!")
    
    await ai.shutdown()

asyncio.run(benchmark())
EOF

python3 benchmark_architecture.py
```

## 8. Monitor What's Happening

```bash
# Watch the logs to see each component work
THINK_AI_LOG_LEVEL=DEBUG python3 demonstrate_proper_architecture.py
```

You'll see:
- Cache checks
- Knowledge base searches
- Vector operations
- Claude API calls (only when needed)
- Cost tracking

## 9. Test Specific Features

### Test Knowledge Persistence
```bash
# Add knowledge, shutdown, restart, verify it's still there
python3 -c "
import asyncio
from implement_proper_architecture import ProperThinkAI

async def test():
    # Session 1: Add knowledge
    ai = ProperThinkAI()
    await ai.initialize()
    await ai._store_fact('Test fact: Think AI remembers everything')
    await ai.shutdown()
    
    # Session 2: Verify persistence
    ai2 = ProperThinkAI()
    await ai2.initialize()
    result = await ai2.process_with_proper_architecture('What does Think AI remember?')
    print('Knowledge persisted:', 'Test fact' in result['response'])
    await ai2.shutdown()

asyncio.run(test())
"
```

### Test Cost Optimization
```bash
# Process many queries and see cost savings
python3 -c "
import asyncio
from implement_proper_architecture import ProperThinkAI

async def cost_test():
    ai = ProperThinkAI()
    await ai.initialize()
    
    # Process 10 queries (mix of unique and duplicates)
    queries = ['What is AI?'] * 3 + ['Explain ML'] * 2 + ['What is AI?'] * 2 + ['New query 1', 'New query 2', 'New query 3']
    
    for q in queries:
        await ai.process_with_proper_architecture(q)
    
    costs = ai.claude.get_cost_summary()
    print(f'Processed {len(queries)} queries')
    print(f'Claude called {costs[\"request_count\"]} times')
    print(f'Cost: ${costs[\"total_cost\"]:.4f}')
    print(f'Traditional cost would be: ${0.02 * len(queries):.4f}')
    print(f'You saved: ${0.02 * len(queries) - costs[\"total_cost\"]:.4f}!')
    
    await ai.shutdown()

asyncio.run(cost_test())
"
```

## 10. Real Interactive Chat Test

Create this file to have a real conversation:

```bash
cat > chat_with_proper_ai.py << 'EOF'
import asyncio
from implement_proper_architecture import ProperThinkAI

async def chat():
    ai = ProperThinkAI()
    await ai.initialize()
    
    print("\n🤖 Think AI with Proper Architecture")
    print("Commands: /cost, /stats, /quit")
    print("-" * 50)
    
    while True:
        query = input("\nYou: ").strip()
        
        if query == '/quit':
            break
        elif query == '/cost':
            costs = ai.claude.get_cost_summary()
            print(f"Total cost: ${costs['total_cost']:.4f}")
            print(f"API calls: {costs['request_count']}")
            continue
        elif query == '/stats':
            # Count cached items
            cache_count = 0
            async for _ in ai.services['scylla'].scan(prefix="cache_", limit=100):
                cache_count += 1
            print(f"Cached responses: {cache_count}")
            print(f"Knowledge entries: {len(ai.knowledge_base)}")
            continue
        
        print("\nThink AI: ", end="", flush=True)
        result = await ai.process_with_proper_architecture(query)
        print(result['response'])
        
        # Show if Claude was used
        if 'claude' in result['architecture_usage']['enhancement']:
            print("\n[Used Claude enhancement]")
        else:
            print("\n[Distributed response only!]")
    
    await ai.shutdown()

asyncio.run(chat())
EOF

python3 chat_with_proper_ai.py
```

## 🎯 What to Look For

1. **Cache Hits** - Ask same question twice, second is instant
2. **Knowledge Usage** - Questions about consciousness, AI ethics use stored facts
3. **Cost Tracking** - Watch costs stay low
4. **Response Speed** - Cached = instant, Knowledge = fast, Claude = slower
5. **Learning** - System stores every interaction

## 💡 Pro Tips

- Ask about topics in knowledge base first (consciousness, ethics, distributed systems)
- Then ask same questions again to see cache
- Try variations to test similarity search
- Use `/stats` to see what's stored
- Check costs with `/cost`

The architecture is working - now you can see it yourself!