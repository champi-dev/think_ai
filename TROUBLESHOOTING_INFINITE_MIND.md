# 🔧 Troubleshooting Infinite Consciousness

## Common Issues and Solutions

### 1. **System Hangs at "Generating response from distributed knowledge..."**

**Symptoms:**
- User asks a question
- System shows processing steps
- Hangs at step 6 without responding

**Causes & Solutions:**

#### A. Ollama Not Responding
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve

# Pre-load the model
ollama run phi3:mini "test"
```

#### B. First Generation Timeout
The first generation after starting can take 30-60 seconds while the model loads into memory.

**Solution:**
```bash
# Pre-warm the model before starting
./start_check_and_run.sh
```

#### C. Model Not Downloaded
```bash
# Check if model exists
ollama list

# Download if missing
ollama pull phi3:mini
```

### 2. **Background Thoughts Not Appearing**

**Symptoms:**
- No consciousness updates showing
- No thoughts being generated

**Solutions:**
```bash
# Check consciousness state
/state

# Inject a thought to stimulate thinking
/think What is the nature of reality?

# Check recent thoughts
/recent
```

### 3. **High Memory Usage**

**Symptoms:**
- System slowing down
- Memory warnings

**Solutions:**
1. Consciousness automatically compresses at 80% capacity
2. Restart to clear memory:
   ```bash
   /quit
   ./start_infinite_consciousness.sh
   ```

### 4. **No Response to User Input**

**Test Ollama First:**
```bash
python3 test_ollama_simple.py
```

**If Ollama test fails:**
1. Restart Ollama: `killall ollama && ollama serve`
2. Check port 11434 is not blocked
3. Try different model: `ollama pull tinyllama`

### 5. **ScyllaDB/Redis Errors**

**Non-critical** - The system will work without them but with limited features:
- No caching (Redis)
- No persistent storage (ScyllaDB)

To run without distributed services:
```bash
# Just run with Ollama
python3 test_ollama_simple.py
# If that works, consciousness will work
```

## Quick Diagnostic Script

```bash
#!/bin/bash
echo "🔍 Diagnosing Think AI..."

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama running"
    if ollama list | grep -q phi3:mini; then
        echo "✅ Phi-3.5 Mini installed"
    else
        echo "❌ Phi-3.5 Mini missing"
    fi
else
    echo "❌ Ollama not running"
fi

# Check services
lsof -i:9042 > /dev/null 2>&1 && echo "✅ ScyllaDB" || echo "⚠️  ScyllaDB not running"
lsof -i:6379 > /dev/null 2>&1 && echo "✅ Redis" || echo "⚠️  Redis not running"

# Test generation
echo "Testing Phi-3.5 generation..."
time ollama run phi3:mini "Say hello" 2>&1 | head -1
```

## Configuration Tweaks

If responses are too slow, edit `implement_proper_architecture.py`:

```python
# Reduce timeout (line ~33)
async with httpx.AsyncClient(timeout=15.0) as client:  # Was 30.0

# Reduce max tokens (line ~463)
model_response = await self.ollama_model.generate(prompt, max_tokens=100)  # Was 200
```

## Fallback Mode

If Ollama consistently fails, the system will use fallback responses based on distributed knowledge. This is intentional to prevent hanging.

## Performance Tips

1. **Pre-load Model**: Always run `ollama run phi3:mini "test"` before starting
2. **Reduce Thinking Interval**: Edit `config/consciousness_config.yaml`:
   ```yaml
   think_interval: 10.0  # Increase from 5.0 to reduce background load
   ```
3. **Disable Background Thinking**: Comment out in `infinite_mind_simple.py`:
   ```python
   # await self.infinite_mind.start()  # Line ~27
   ```

## Still Having Issues?

1. Run the simple Ollama test:
   ```bash
   python3 test_ollama_simple.py
   ```

2. Try the basic chat without consciousness:
   ```bash
   python3 interactive_chat_phi35.py
   ```

3. Check logs:
   ```bash
   # Look for errors in the output
   grep -i error *.log
   ```

The system is designed to be resilient - if one component fails, others continue working!