
import sys
import json

results = {}

# Test imports
try:
    import think_ai
    results["import_think_ai"] = {"success": True, "version": getattr(think_ai, "__version__", "unknown")}
except Exception as e:
    results["import_think_ai"] = {"success": False, "error": str(e)}

try:
    import think_ai_cli
    results["import_think_ai_cli"] = {"success": True}
except Exception as e:
    results["import_think_ai_cli"] = {"success": False, "error": str(e)}

try:
    import o1_vector_search
    results["import_o1_vector_search"] = {"success": True}
except Exception as e:
    results["import_o1_vector_search"] = {"success": False, "error": str(e)}

# Test core functionality
try:
    from think_ai import ThinkAI
    ai = ThinkAI()
    response = ai.chat("Test message")
    results["think_ai_chat"] = {"success": True, "response_length": len(response)}
except Exception as e:
    results["think_ai_chat"] = {"success": False, "error": str(e)}

# Test vector search
try:
    from o1_vector_search import O1VectorSearch
    search = O1VectorSearch(dimensions=128)
    search.add("test1", [0.1] * 128, {"content": "Test 1"})
    results["o1_vector_search"] = {"success": True}
except Exception as e:
    results["o1_vector_search"] = {"success": False, "error": str(e)}

print(json.dumps(results))
