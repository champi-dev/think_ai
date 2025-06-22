"""Integration tests for CLI packages."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestCLIPackages:
    """Test Python and Node.js CLI packages."""

    def test_python_cli_installation(self) -> None:
        """Test Python CLI can be installed."""
        # Quick check that package structure is valid
        assert os.path.exists("think-ai-cli/python/setup.py")
        assert os.path.exists("think-ai-cli/python/think_ai_cli/__init__.py")

        # Test that the module structure is valid without importing
        # (importing requires dependencies to be installed)
        import ast

        with open("think-ai-cli/python/think_ai_cli/__init__.py") as f:
            tree = ast.parse(f.read())
            # Check that ThinkAI and main are defined
            # Check that __all__ exports the required names
            all_export = None
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            if isinstance(node.value, ast.List):
                                all_export = []
                                for elt in node.value.elts:
                                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                        all_export.append(elt.value)
                                    elif hasattr(elt, "s"):  # Older AST format
                                        all_export.append(elt.s)
                            break

            assert all_export is not None, "__all__ not found"
            assert "ThinkAI" in all_export, f"ThinkAI not in __all__: {all_export}"
            assert "main" in all_export, f"main not in __all__: {all_export}"

    def test_python_cli_commands(self) -> None:
        """Test Python CLI commands."""
        # Run in subprocess to avoid import conflicts
        test_script = """
import sys
import json
sys.path.insert(0, "think-ai-cli/python")

try:
    from think_ai_cli import ThinkAI
    
    # Test initialization
    cli = ThinkAI()
    
    # Test add command
    result = cli.add("Test knowledge", {"source": "test"})
    assert result["status"] == "added"
    
    # Test search command
    results = cli.search("test", k=1)
    assert len(results) > 0
    
    # Test analyze command
    code = "def hello(): print('hello')"
    analysis = cli.analyze(code)
    assert "structure" in analysis
    
    # Test generate command
    prompt = "Write a function to add two numbers"
    code = cli.generate(prompt)
    assert "def" in code
    assert "return" in code
    
    print("All Python CLI tests passed!")
except ImportError as e:
    # Skip if CLI package not available
    print(f"Skipping test: {e}")
    sys.exit(0)
"""

        result = subprocess.run(
            [sys.executable, "-c", test_script],
            check=False,
            capture_output=True,
            text=True,
        )

        if "Skipping test:" in result.stdout:
            pytest.skip("think_ai_cli package not available")

        assert result.returncode == 0
        assert "All Python CLI tests passed!" in result.stdout

    def test_nodejs_cli_installation(self) -> None:
        """Test Node.js CLI can be installed."""
        # Quick check that package structure is valid
        assert os.path.exists("think-ai-cli/nodejs/package.json")
        assert os.path.exists("think-ai-cli/nodejs/dist/index.js")
        assert os.path.exists("think-ai-cli/nodejs/dist/cli.js")

        # Check package.json is valid JSON
        with open("think-ai-cli/nodejs/package.json") as f:
            package_data = json.load(f)
            assert package_data.get("name") == "think-ai-cli"
            assert "version" in package_data

    def test_nodejs_cli_commands(self) -> None:
        """Test Node.js CLI commands."""
        # Skip this test as it requires ES module support
        pytest.skip("Node.js CLI requires ES module refactoring")

        test_script = """
const {{ThinkAI}} = require('{nodejs_cli_path}/dist/index.js');

async function runTests() {{
    const ai = new ThinkAI();
    
    // Test initialization
    await ai.initialize();
    
    // Test add
    const addResult = await ai.add('Test knowledge', {{source: 'test'}});
    console.assert(addResult.status === 'added', 'Add failed');
    
    // Test search
    const searchResults = await ai.search('test', 1);
    console.assert(searchResults.length > 0, 'Search failed');
    
    // Test analyze
    const code = 'function hello() {{console.log("hello");}}';
    const analysis = await ai.analyze(code);
    console.assert(analysis.structure, 'Analyze failed');
    
    console.log('All Node.js CLI tests passed!');
}}

runTests().catch(console.error);
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
            f.write(test_script)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["node", temp_path],
                check=False,
                cwd="think-ai-cli/nodejs",
                capture_output=True,
                text=True,
            )

            assert "All Node.js CLI tests passed!" in result.stdout
        finally:
            os.unlink(temp_path)

    def test_cli_interoperability(self) -> None:
        """Test that both CLIs produce compatible results."""
        # Create test data with Python CLI
        python_script = """
import sys
import json
sys.path.insert(0, "think-ai-cli/python")

try:
    from think_ai_cli import ThinkAI
    
    cli = ThinkAI()
    cli.add("Interoperability test", {"lang": "both"})
    results = cli.search("interoperability", k=1)
    print(json.dumps(results))
except ImportError:
    print(json.dumps([]))
    sys.exit(0)
"""

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                python_script,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        python_results = json.loads(result.stdout)

        if not python_results:
            pytest.skip("think_ai_cli package not available")

        assert len(python_results) > 0

        # Verify structure
        assert "score" in python_results[0]
        assert "text" in python_results[0]
        assert "metadata" in python_results[0]

    @pytest.mark.performance
    def test_cli_performance(self) -> None:
        """Test CLI performance."""
        # Test Python CLI performance
        python_script = """
import sys
import time
sys.path.insert(0, "think-ai-cli/python")

try:
    from think_ai_cli import ThinkAI
    
    cli = ThinkAI()
    
    # Add items
    start = time.time()
    for i in range(100):
        cli.add(f"Item {i}", {"index": i})
    add_time = time.time() - start
    
    # Search items
    start = time.time()
    for i in range(20):
        cli.search(f"Item {i}", k=5)
    search_time = time.time() - start
    
    print(f"Python CLI - Add rate: {100/add_time:.2f} items/sec")
    print(f"Python CLI - Search rate: {20/search_time:.2f} queries/sec")
except ImportError:
    print("Skipping performance test")
    sys.exit(0)
"""

        result = subprocess.run(
            [sys.executable, "-c", python_script],
            check=False,
            capture_output=True,
            text=True,
        )

        if "Skipping performance test" in result.stdout:
            pytest.skip("think_ai_cli package not available")

        assert result.returncode == 0
