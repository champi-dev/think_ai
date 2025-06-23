# Think AI CLI Examples & Cookbook

## Table of Contents
1. [Quick Start Examples](#quick-start-examples)
2. [Real-World Use Cases](#real-world-use-cases)
3. [Advanced Patterns](#advanced-patterns)
4. [Integration Examples](#integration-examples)
5. [Performance Optimization](#performance-optimization)
6. [Troubleshooting Scenarios](#troubleshooting-scenarios)

## Quick Start Examples

### Your First Think AI Session
```bash
# Start Think AI with default settings
$ think-ai

Welcome to Think AI CLI! 🧠
Type /help for available commands.

> Hello, Think AI!
Hello! I'm Think AI, your O(1) performance AI assistant. How can I help you today?

> /store python_tips "Use list comprehensions for cleaner code"
✓ Stored: python_tips -> Use list comprehensions for cleaner code

> /query What's a good Python tip?
Based on stored knowledge: Use list comprehensions for cleaner code. 
They're more readable and often faster than traditional loops.

> /memory
Memory Usage:
- Active entries: 1
- Total size: 48 bytes
- Performance: 0.15ms average query time

> /exit
Goodbye! Session saved.
```

### Different CLI Modes Comparison
```bash
# 1. Simple O(1) Chat (No API, instant responses)
$ think-ai-chat
Think AI Simple Chat (O(1) Mode)
Type 'help' for commands, 'exit' to quit.

You: What is recursion?
AI: [0.12ms] Recursion is a programming technique where a function calls itself to solve a problem by breaking it into smaller subproblems.

# 2. Full System (All features enabled)
$ think-ai-full
Think AI Full System v1.0.0
All components loaded: ✓ Consciousness ✓ Knowledge ✓ Vector Search

> demonstrate consciousness
[Consciousness: Analytical] Analyzing request pattern...
[Consciousness: Creative] Generating unique demonstration...
[Consciousness: Empathetic] I understand you'd like to see how consciousness states work!

# 3. API Server (RESTful interface)
$ think-ai-server --port 8080
INFO: Starting Think AI API Server
INFO: Uvicorn running on http://0.0.0.0:8080
```

## Real-World Use Cases

### 1. Personal Knowledge Assistant
Build your personal knowledge base:

```bash
#!/bin/bash
# knowledge_assistant.sh

# Start Think AI and load personal notes
think-ai << 'EOF'
/store meeting_notes "Weekly standup at 10am Mondays"
/store project_deadlines "MVP due March 15, Beta April 1"
/store team_contacts "John (PM): john@example.com, Sarah (Dev): sarah@example.com"
/store coding_standards "Use Black formatter, 100% test coverage required"

/query When is the weekly standup?
/query What are our coding standards?
/search deadlines
/export my_knowledge_base.json
/exit
EOF
```

### 2. Code Review Assistant
Interactive code review helper:

```python
# code_review.py
import subprocess
import json

def review_code(file_path):
    """Use Think AI to review code"""
    
    with open(file_path, 'r') as f:
        code = f.read()
    
    # Store code context
    commands = [
        f'/store current_file "{file_path}"',
        f'/store code_snippet "{code[:500]}"',  # First 500 chars
        '/consciousness analytical',  # Set analytical mode
        '/query Review this code for potential issues, focusing on performance and security',
        '/query Suggest improvements for code readability',
        '/export code_review_results.json',
        '/exit'
    ]
    
    result = subprocess.run(
        ['think-ai', '--budget', 'minimal'],
        input='\n'.join(commands),
        capture_output=True,
        text=True
    )
    
    return result.stdout

# Usage
review_output = review_code('my_module.py')
print(review_output)
```

### 3. Documentation Generator
Auto-generate documentation from code:

```bash
# doc_generator.sh
#!/bin/bash

# Function to generate docs for Python files
generate_docs() {
    local file=$1
    local module_name=$(basename "$file" .py)
    
    echo "Generating documentation for $module_name..."
    
    think-ai --no-restore << EOF
/store file_path "$file"
/store module_name "$module_name"

/query Generate comprehensive documentation for module $module_name including:
- Module overview
- Function descriptions  
- Usage examples
- Parameter explanations

/export "docs/${module_name}_documentation.md"
/exit
EOF
}

# Process all Python files
for file in src/*.py; do
    generate_docs "$file"
done
```

### 4. Learning Companion
Interactive learning sessions:

```python
# learning_companion.py
import asyncio
from think_ai import ThinkAIEngine

async def learning_session(topic):
    """Interactive learning session on any topic"""
    
    engine = ThinkAIEngine(budget_profile='minimal')
    
    # Set up learning context
    await engine.store(f'{topic}_level', 'beginner')
    await engine.store(f'{topic}_goal', 'understand fundamentals')
    
    # Start interactive session
    print(f"🎓 Learning Session: {topic}")
    print("Commands: 'explain', 'example', 'quiz', 'deeper', 'done'")
    
    while True:
        command = input("\nWhat would you like to do? ").strip().lower()
        
        if command == 'done':
            break
        elif command == 'explain':
            response = await engine.query(f"Explain {topic} for beginners")
        elif command == 'example':
            response = await engine.query(f"Give a practical example of {topic}")
        elif command == 'quiz':
            response = await engine.query(f"Create a quiz question about {topic}")
        elif command == 'deeper':
            await engine.store(f'{topic}_level', 'intermediate')
            response = await engine.query(f"Explain advanced concepts in {topic}")
        else:
            response = "Unknown command. Try: explain, example, quiz, deeper, done"
        
        print(f"\n{response}")
    
    # Save learning progress
    await engine.export(f"learning_{topic}.json")
    print(f"\n✅ Learning session saved to learning_{topic}.json")

# Run learning session
asyncio.run(learning_session("machine learning"))
```

### 5. Daily Standup Assistant
Automate daily standup reports:

```bash
#!/bin/bash
# daily_standup.sh

DATE=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

think-ai --budget minimal << EOF
# Load context
/store current_date "$DATE"
/store yesterday_date "$YESTERDAY"
/search tasks_$YESTERDAY

# Generate standup
/consciousness creative
/query Generate a daily standup report with:
1. What I accomplished yesterday
2. What I plan to do today  
3. Any blockers or concerns

# Save for future reference
/store standup_$DATE "Generated standup report"
/export "standups/standup_$DATE.md"

# Send to Slack (optional)
/query Format this standup for Slack with appropriate emoji

/exit
EOF
```

## Advanced Patterns

### 1. Multi-Stage Processing Pipeline
Complex data processing with state management:

```python
# pipeline_processor.py
import asyncio
from think_ai import ThinkAIEngine

class DataPipeline:
    def __init__(self):
        self.engine = ThinkAIEngine(budget_profile='balanced')
        self.stages = []
    
    async def add_stage(self, name, processor):
        """Add processing stage"""
        self.stages.append((name, processor))
        await self.engine.store(f'pipeline_stage_{name}', 'registered')
    
    async def process(self, data):
        """Process data through all stages"""
        result = data
        
        for stage_name, processor in self.stages:
            # Store intermediate result
            await self.engine.store(f'stage_{stage_name}_input', str(result))
            
            # Process with consciousness state
            if 'analyze' in stage_name:
                await self.engine.set_consciousness('analytical')
            elif 'create' in stage_name:
                await self.engine.set_consciousness('creative')
            
            # Process stage
            result = await processor(result, self.engine)
            
            # Store output
            await self.engine.store(f'stage_{stage_name}_output', str(result))
        
        return result

# Example usage
async def analyze_text(text, engine):
    response = await engine.query(f"Analyze sentiment and key themes in: {text}")
    return response

async def generate_summary(analysis, engine):
    response = await engine.query(f"Create executive summary from: {analysis}")
    return response

# Run pipeline
pipeline = DataPipeline()
await pipeline.add_stage('analyze', analyze_text)
await pipeline.add_stage('summarize', generate_summary)

result = await pipeline.process("Your text data here...")
```

### 2. Intelligent Caching Strategy
Optimize API usage with smart caching:

```python
# smart_cache.py
import hashlib
import json
from datetime import datetime, timedelta

class SmartCache:
    def __init__(self, think_ai_engine):
        self.engine = think_ai_engine
        self.cache_duration = timedelta(hours=24)
    
    async def get_or_compute(self, query, force_refresh=False):
        """Get from cache or compute with Think AI"""
        
        # Generate cache key
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        if not force_refresh:
            # Try to get from cache
            cached = await self.engine.search(f"cache_{cache_key}")
            
            if cached:
                cache_data = json.loads(cached[0]['value'])
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                
                if datetime.now() - cache_time < self.cache_duration:
                    print(f"✓ Cache hit for: {query[:50]}...")
                    return cache_data['response']
        
        # Compute new response
        print(f"⟳ Computing response for: {query[:50]}...")
        response = await self.engine.query(query)
        
        # Store in cache
        cache_data = {
            'query': query,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        
        await self.engine.store(
            f"cache_{cache_key}", 
            json.dumps(cache_data)
        )
        
        return response

# Usage
cache = SmartCache(engine)
response = await cache.get_or_compute("Explain quantum computing")
```

### 3. Batch Processing with Progress
Process multiple items efficiently:

```bash
#!/bin/bash
# batch_processor.sh

# Process multiple files with progress tracking
process_batch() {
    local files=("$@")
    local total=${#files[@]}
    local current=0
    
    # Start Think AI session
    {
        echo "/consciousness analytical"
        echo "/store batch_size $total"
        echo "/store batch_start $(date -Iseconds)"
        
        for file in "${files[@]}"; do
            ((current++))
            echo "/store current_file \"$file\""
            echo "/store progress \"$current/$total\""
            echo "/query Analyze file $file and suggest improvements"
            echo "/store result_$file \"Analysis complete\""
        done
        
        echo "/store batch_end $(date -Iseconds)"
        echo "/query Generate batch processing summary report"
        echo "/export batch_results.json"
        echo "/exit"
    } | think-ai --budget balanced
}

# Process all Python files in src/
process_batch src/*.py
```

### 4. Context-Aware Conversations
Maintain context across multiple queries:

```python
# context_conversation.py
class ContextualConversation:
    def __init__(self, engine):
        self.engine = engine
        self.context_window = 5  # Remember last 5 exchanges
        self.history = []
    
    async def ask(self, question):
        """Ask with context awareness"""
        
        # Build context from history
        context = "\n".join([
            f"Q: {h['question']}\nA: {h['answer'][:100]}..."
            for h in self.history[-self.context_window:]
        ])
        
        # Store context
        await self.engine.store('conversation_context', context)
        
        # Add context to query
        if self.history:
            contextual_query = f"Given our previous discussion:\n{context}\n\nNow answer: {question}"
        else:
            contextual_query = question
        
        # Get response
        answer = await self.engine.query(contextual_query)
        
        # Update history
        self.history.append({
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })
        
        return answer

# Usage
conv = ContextualConversation(engine)
await conv.ask("What is machine learning?")
await conv.ask("How does it relate to AI?")  # Will remember previous context
await conv.ask("Give me a practical example")  # Knows we're talking about ML
```

## Integration Examples

### 1. Slack Bot Integration
```python
# slack_bot.py
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import asyncio
from think_ai import ThinkAIEngine

class ThinkAISlackBot:
    def __init__(self, slack_token, think_ai_budget='minimal'):
        self.slack = WebClient(token=slack_token)
        self.engine = ThinkAIEngine(budget_profile=think_ai_budget)
    
    async def handle_message(self, channel, text, user):
        """Process Slack message with Think AI"""
        
        # Store context
        await self.engine.store(f'slack_user_{user}', 'active')
        await self.engine.store('slack_channel', channel)
        
        # Process message
        if text.startswith('!think'):
            query = text[6:].strip()
            response = await self.engine.query(query)
            
            # Send response
            try:
                self.slack.chat_postMessage(
                    channel=channel,
                    text=f"🧠 {response}",
                    thread_ts=None  # Start new thread
                )
            except SlackApiError as e:
                print(f"Slack error: {e}")

# Usage
bot = ThinkAISlackBot(slack_token="xoxb-...")
await bot.handle_message("#general", "!think explain Docker", "U123456")
```

### 2. VS Code Extension
```javascript
// vscode_extension.js
const vscode = require('vscode');
const { spawn } = require('child_process');

function activate(context) {
    // Register command
    let disposable = vscode.commands.registerCommand('thinkAI.askQuestion', async () => {
        // Get user input
        const question = await vscode.window.showInputBox({
            prompt: 'Ask Think AI a question',
            placeHolder: 'e.g., How do I optimize this function?'
        });
        
        if (!question) return;
        
        // Get current file context
        const editor = vscode.window.activeTextEditor;
        const fileName = editor ? editor.document.fileName : 'No file';
        const selection = editor ? editor.document.getText(editor.selection) : '';
        
        // Call Think AI CLI
        const thinkAI = spawn('think-ai', ['--no-restore']);
        
        // Send commands
        thinkAI.stdin.write(`/store current_file "${fileName}"\n`);
        if (selection) {
            thinkAI.stdin.write(`/store selected_code "${selection.substring(0, 500)}"\n`);
        }
        thinkAI.stdin.write(`/query ${question}\n`);
        thinkAI.stdin.write('/exit\n');
        
        // Collect output
        let output = '';
        thinkAI.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        thinkAI.on('close', () => {
            // Show result
            vscode.window.showInformationMessage(`Think AI: ${output}`);
        });
    });
    
    context.subscriptions.push(disposable);
}

module.exports = { activate };
```

### 3. GitHub Actions Integration
```yaml
# .github/workflows/think-ai-review.yml
name: Think AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Think AI
        run: |
          pip install think-ai-consciousness
      
      - name: Run AI Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Get changed files
          CHANGED_FILES=$(git diff --name-only ${{ github.event.before }}..${{ github.sha }})
          
          # Review each file
          for file in $CHANGED_FILES; do
            if [[ $file == *.py ]]; then
              think-ai --budget minimal << EOF
          /store pr_number "${{ github.event.number }}"
          /store file_path "$file"
          /consciousness analytical
          /query Review this Python file for:
          - Security vulnerabilities
          - Performance issues  
          - Code style violations
          - Missing error handling
          /export "review_${file//\//_}.json"
          /exit
          EOF
            fi
          done
      
      - name: Post Review Comments
        uses: actions/github-script@v6
        with:
          script: |
            // Read review results and post as PR comments
            const fs = require('fs');
            const reviews = fs.readdirSync('.')
              .filter(f => f.startsWith('review_'))
              .map(f => JSON.parse(fs.readFileSync(f)));
            
            for (const review of reviews) {
              await github.rest.pulls.createReviewComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: context.issue.number,
                body: review.analysis,
                path: review.file_path,
                line: 1
              });
            }
```

### 4. Jupyter Notebook Integration
```python
# think_ai_notebook.ipynb

# Cell 1: Setup
!pip install think-ai-consciousness
from think_ai import ThinkAIEngine
import asyncio

# Cell 2: Initialize
engine = ThinkAIEngine(budget_profile='minimal')

# Cell 3: Interactive helper
class NotebookAI:
    def __init__(self, engine):
        self.engine = engine
        
    async def explain_cell(self, code):
        """Explain what a code cell does"""
        response = await self.engine.query(
            f"Explain this code in simple terms:\n{code}"
        )
        return response
    
    async def debug_error(self, error):
        """Help debug an error"""
        response = await self.engine.query(
            f"Help me fix this error:\n{error}"
        )
        return response
    
    async def optimize_code(self, code):
        """Suggest optimizations"""
        await self.engine.set_consciousness('analytical')
        response = await self.engine.query(
            f"Optimize this code for performance:\n{code}"
        )
        return response

# Cell 4: Usage
ai = NotebookAI(engine)

# Get help with the previous cell's code
code = In[-1]  # Get previous cell input
explanation = await ai.explain_cell(code)
print(explanation)

# Debug an error
try:
    # Your code that causes error
    result = 1/0
except Exception as e:
    help_text = await ai.debug_error(str(e))
    print(help_text)
```

## Performance Optimization

### 1. Minimizing API Calls
```python
# Batch multiple queries efficiently
class BatchProcessor:
    def __init__(self, engine):
        self.engine = engine
        self.batch = []
        self.batch_size = 10
    
    async def add_query(self, query):
        """Add query to batch"""
        self.batch.append(query)
        
        if len(self.batch) >= self.batch_size:
            return await self.process_batch()
    
    async def process_batch(self):
        """Process all queries in batch"""
        if not self.batch:
            return []
        
        # Combine queries
        combined = "\n\n".join([
            f"Query {i+1}: {q}"
            for i, q in enumerate(self.batch)
        ])
        
        # Single API call
        response = await self.engine.query(
            f"Answer these {len(self.batch)} queries:\n{combined}"
        )
        
        # Clear batch
        self.batch = []
        
        return response
```

### 2. Local Caching Layer
```bash
#!/bin/bash
# cache_layer.sh

# Create local cache directory
CACHE_DIR="$HOME/.think_ai_cache"
mkdir -p "$CACHE_DIR"

# Function to get cached or fresh response
cached_query() {
    local query="$1"
    local cache_key=$(echo -n "$query" | md5sum | cut -d' ' -f1)
    local cache_file="$CACHE_DIR/$cache_key"
    
    # Check cache (valid for 1 day)
    if [[ -f "$cache_file" ]] && [[ $(find "$cache_file" -mtime -1) ]]; then
        echo "# Cached response:"
        cat "$cache_file"
    else
        # Get fresh response
        response=$(echo "/query $query" | think-ai --no-restore | tail -n +3)
        echo "$response" > "$cache_file"
        echo "# Fresh response:"
        echo "$response"
    fi
}

# Usage
cached_query "What is machine learning?"
```

### 3. Parallel Processing
```python
# parallel_processor.py
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelThinkAI:
    def __init__(self, num_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.engines = [
            ThinkAIEngine(budget_profile='minimal')
            for _ in range(num_workers)
        ]
    
    async def process_many(self, queries):
        """Process multiple queries in parallel"""
        
        async def process_one(engine, query):
            return await engine.query(query)
        
        # Create tasks
        tasks = []
        for i, query in enumerate(queries):
            engine = self.engines[i % len(self.engines)]
            task = asyncio.create_task(process_one(engine, query))
            tasks.append(task)
        
        # Wait for all to complete
        results = await asyncio.gather(*tasks)
        return results

# Usage
processor = ParallelThinkAI(num_workers=4)
queries = [
    "Explain Python decorators",
    "What is async/await?",
    "How does garbage collection work?",
    "Explain list comprehensions"
]
results = await processor.process_many(queries)
```

## Troubleshooting Scenarios

### 1. Handling API Failures
```python
# resilient_client.py
import asyncio
from typing import Optional

class ResilientThinkAI:
    def __init__(self):
        self.primary = ThinkAIEngine(budget_profile='balanced')
        self.fallback = ThinkAIEngine(budget_profile='free_tier')
        self.local_mode = False
    
    async def query_with_fallback(self, text: str) -> str:
        """Query with automatic fallback"""
        
        try:
            # Try primary engine
            if not self.local_mode:
                return await self.primary.query(text)
        except Exception as e:
            print(f"Primary engine failed: {e}")
            
        try:
            # Try fallback engine
            return await self.fallback.query(text)
        except Exception as e:
            print(f"Fallback engine failed: {e}")
            
        # Final fallback: local hash-based response
        self.local_mode = True
        return self.local_response(text)
    
    def local_response(self, text: str) -> str:
        """Generate local response without API"""
        # Simple hash-based response
        responses = {
            'hello': 'Hello! How can I help you?',
            'help': 'Available commands: /query, /store, /search, /exit',
            # Add more as needed
        }
        
        key = text.lower().split()[0] if text else 'help'
        return responses.get(key, 'I understand. Please elaborate.')
```

### 2. Memory Management
```bash
#!/bin/bash
# memory_manager.sh

# Monitor Think AI memory usage
monitor_memory() {
    while true; do
        # Get Think AI process
        PID=$(pgrep -f "think-ai")
        
        if [[ -n "$PID" ]]; then
            # Get memory usage
            MEM=$(ps -p "$PID" -o %mem=)
            
            # Alert if high
            if (( $(echo "$MEM > 10.0" | bc -l) )); then
                echo "⚠️  High memory usage: ${MEM}%"
                
                # Clear cache
                think-ai << EOF
/memory
/clear
/store memory_cleared "$(date)"
/exit
EOF
            fi
        fi
        
        sleep 60
    done
}

# Run monitor in background
monitor_memory &
```

### 3. Debugging Connection Issues
```python
# connection_debugger.py
import aiohttp
import asyncio
from urllib.parse import urlparse

class ConnectionDebugger:
    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    async def diagnose(self):
        """Diagnose connection issues"""
        
        tests = {
            'DNS': self.test_dns,
            'Internet': self.test_internet,
            'API Endpoint': self.test_api,
            'Firewall': self.test_firewall,
            'Proxy': self.test_proxy
        }
        
        results = {}
        for name, test in tests.items():
            try:
                result = await test()
                results[name] = {'status': 'OK', 'details': result}
            except Exception as e:
                results[name] = {'status': 'FAIL', 'error': str(e)}
        
        return results
    
    async def test_dns(self):
        """Test DNS resolution"""
        import socket
        socket.gethostbyname('api.anthropic.com')
        return "DNS resolution working"
    
    async def test_internet(self):
        """Test general internet connectivity"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.google.com') as resp:
                return f"Internet accessible (status: {resp.status})"
    
    async def test_api(self):
        """Test API endpoint"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.anthropic.com/v1/health') as resp:
                return f"API reachable (status: {resp.status})"
    
    async def test_firewall(self):
        """Check common firewall issues"""
        ports = [80, 443, 8080]
        open_ports = []
        
        for port in ports:
            try:
                # Simple connection test
                reader, writer = await asyncio.open_connection('api.anthropic.com', port)
                writer.close()
                await writer.wait_closed()
                open_ports.append(port)
            except:
                pass
        
        return f"Open ports: {open_ports}"
    
    async def test_proxy(self):
        """Check proxy settings"""
        import os
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY']
        settings = {var: os.environ.get(var, 'Not set') for var in proxy_vars}
        return f"Proxy settings: {settings}"

# Run diagnostics
debugger = ConnectionDebugger()
results = await debugger.diagnose()

print("Connection Diagnostics:")
for test, result in results.items():
    status = "✓" if result['status'] == 'OK' else "✗"
    print(f"{status} {test}: {result.get('details', result.get('error'))}")
```

This comprehensive examples and cookbook provides practical, real-world scenarios for using Think AI CLI effectively across various use cases and integration patterns.