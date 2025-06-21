
import json
import sys

results = {"imports": {}, "functionality": {}}

# Test imports
libraries = [
    ("think_ai", "think-ai-consciousness"),
    ("think_ai_cli", "think-ai-cli"),
    ("o1_vector_search", "o1-vector-search")
]

for module_name, lib_name in libraries:
    try:
        module = __import__(module_name)
        results["imports"][lib_name] = {
            "success": True,
            "version": getattr(module, "__version__", "unknown")
        }
    except Exception as e:
        results["imports"][lib_name] = {
            "success": False,
            "error": str(e)
        }

# Test Think AI functionality
try:
    from think_ai import ThinkAI
    ai = ThinkAI()
    response = ai.chat("Test: What is 2+2?")
    results["functionality"]["think_ai_chat"] = {
        "success": True,
        "response_received": bool(response),
        "response_length": len(response) if response else 0
    }
except Exception as e:
    results["functionality"]["think_ai_chat"] = {
        "success": False,
        "error": str(e)
    }

# Test vector search
try:
    from o1_vector_search import O1VectorSearch
    search = O1VectorSearch(dimensions=128)
    search.add("test1", [0.1] * 128, {"content": "Test document"})
    search.add("test2", [0.2] * 128, {"content": "Another document"})
    
    results_list = search.search([0.15] * 128, k=1)
    results["functionality"]["vector_search"] = {
        "success": True,
        "items_added": 2,
        "search_results": len(results_list)
    }
except Exception as e:
    results["functionality"]["vector_search"] = {
        "success": False,
        "error": str(e)
    }

# Test CLI
try:
    import subprocess
    result = subprocess.run(["think-ai", "--version"], capture_output=True, text=True)
    results["functionality"]["cli"] = {
        "success": result.returncode == 0,
        "output": result.stdout.strip()
    }
except Exception as e:
    results["functionality"]["cli"] = {
        "success": False,
        "error": str(e)
    }

print(json.dumps(results))
