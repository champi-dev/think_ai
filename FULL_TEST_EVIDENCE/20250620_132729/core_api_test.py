
import sys
import json

try:
    # Import based on what's available
    try:
        from think_ai_cli import ThinkAI
    except ImportError:
        try:
            from think_ai_cli.core import ThinkAI
        except ImportError:
            from think_ai_cli.core_annoy import ThinkAI
    
    # Initialize
    ai = ThinkAI()
    results = {"tests": []}
    
    # Test 1: Add code
    try:
        idx = ai.add_code(
            "def hello_world():\n    return 'Hello, World!'",
            "python",
            "Classic hello world function"
        )
        results["tests"].append({
            "name": "add_code",
            "passed": True,
            "index": idx
        })
    except Exception as e:
        results["tests"].append({
            "name": "add_code",
            "passed": False,
            "error": str(e)
        })
    
    # Test 2: Search
    try:
        search_results = ai.search("hello", k=3)
        results["tests"].append({
            "name": "search",
            "passed": len(search_results) > 0,
            "count": len(search_results)
        })
    except Exception as e:
        results["tests"].append({
            "name": "search",
            "passed": False,
            "error": str(e)
        })
    
    # Test 3: Generate code
    try:
        generated = ai.generate_code("create a function to add two numbers")
        results["tests"].append({
            "name": "generate",
            "passed": len(generated) > 0,
            "length": len(generated)
        })
    except Exception as e:
        results["tests"].append({
            "name": "generate",
            "passed": False,
            "error": str(e)
        })
    
    # Test 4: Analyze code
    try:
        analysis = ai.analyze_code("def test():\n    pass")
        results["tests"].append({
            "name": "analyze",
            "passed": "lines" in analysis,
            "lines": analysis.get("lines", 0)
        })
    except Exception as e:
        results["tests"].append({
            "name": "analyze",
            "passed": False,
            "error": str(e)
        })
    
    # Test 5: Get stats
    try:
        stats = ai.get_stats()
        results["tests"].append({
            "name": "stats",
            "passed": "total_snippets" in stats,
            "snippets": stats.get("total_snippets", 0)
        })
    except Exception as e:
        results["tests"].append({
            "name": "stats",
            "passed": False,
            "error": str(e)
        })
    
    print(json.dumps(results))
    sys.exit(0)
    
except Exception as e:
    print(json.dumps({"error": str(e), "tests": []}))
    sys.exit(1)
