"""Integration tests for CLI packages."""

import json
import os
import subprocess
import sys

import pytest
import tempfile

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestCLIPackages:
    """Test Python and
    Node.js CLI packages."""

    def test_python_cli_installation(self) -> None:
        """Test Python CLI can be installed."""
        # Create virtual environment
        with tempfile.TemporaryDirectory() as tmpdir:
            venv_path = os.path.join(tmpdir, "venv")

            # Create virtual environment
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

            # Get pip path
            pip_path = (
                os.path.join(venv_path, "bin", "pip")
                if os.name != "nt"
                else os.path.join(venv_path, "Scripts", "pip.exe")
            )

            # Install the package
            result = subprocess.run(
                [pip_path, "install", "./think-ai-cli/python"],
                check=False,
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0

            # Check if CLI is available
            python_path = (
                os.path.join(venv_path, "bin", "python")
                if os.name != "nt"
                else os.path.join(venv_path, "Scripts", "python.exe")
            )
            result = subprocess.run(
                [python_path, "-m", "think_ai_cli", "--help"],
                check=False,
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            assert "Think AI CLI" in result.stdout

            def test_python_cli_commands(self) -> None:
                """Test Python CLI commands."""
                # Run in subprocess to avoid import conflicts
                test_script = """
                sys.path.insert(0,
                    "think-ai-cli/python")

                # Test initialization
                cli = ThinkAICLI()

                # Test add command
                result = cli.add("Test knowledge",
                    {"source": "test"})
                assert result["status"] == "added"

                # Test search command
                results = cli.search("test",
                    k=1)
                assert len(results) > 0

                # Test analyze command
                code = "def hello(
                    ): print('hello')"
                analysis = cli.analyze(
                    code)
                assert "structure" in analysis

                # Test generate command
                prompt = "Write a function to add two numbers"
                code = cli.generate(
                    prompt)
                assert "def" in code
                assert "return" in code

                print(
                    "All Python CLI tests passed!")
                """

                result = subprocess.run(
                    [sys.executable, "-c", test_script],
                    check=False,
                    capture_output=True,
                    text=True,
                )

                assert result.returncode == 0
                assert "All Python CLI tests passed!" in result.stdout

                def test_nodejs_cli_installation(self) -> None:
                    """Test Node.js CLI can be installed."""
                    # Check if npm is available
                    try:
                        subprocess.run(
                            ["npm", "--version"], check=True, capture_output=True
                        )
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        pytest.skip("npm not available")

                        with tempfile.TemporaryDirectory() as tmpdir:
                            # Copy package to temp dir
                            subprocess.run(
                                ["cp", "-r", "think-ai-cli/nodejs", tmpdir],
                                check=True,
                            )

                            # Install dependencies
                            result = subprocess.run(
                                ["npm", "install"],
                                check=False,
                                cwd=os.path.join(tmpdir, "nodejs"),
                                capture_output=True,
                                text=True,
                            )

                            assert result.returncode == 0

                            # Test CLI
                            result = subprocess.run(
                                ["node", "cli.js", "--help"],
                                check=False,
                                cwd=os.path.join(tmpdir, "nodejs"),
                                capture_output=True,
                                text=True,
                            )

                            assert result.returncode == 0
                            assert "Think AI CLI" in result.stdout

                            def test_nodejs_cli_commands(self) -> None:
                                """Test Node.js CLI commands."""
                                # Check if node is available
                                try:
                                    subprocess.run(
                                        ["node", "--version"],
                                        check=True,
                                        capture_output=True,
                                    )
                                except (
                                    subprocess.CalledProcessError,
                                    FileNotFoundError,
                                ):
                                    pytest.skip("node not available")

                                    test_script = """
                                    const {ThinkAI} = require(
                                        './index.js');

                                    async function runTests(
                                        ) {
                                    const ai = new ThinkAI(
                                        );

                                    // Test initialization
                                    await ai.initialize(
                                        );

                                    // Test add
                                    const addResult = await ai.add('Test knowledge',
                                        {source: 'test'});
                                    console.assert(addResult.status == = 'added',
                                        'Add failed');

                                    // Test search
                                    const searchResults = await ai.search('test',
                                        1);
                                    console.assert(searchResults.length > 0,
                                        'Search failed');

                                    // Test analyze
                                    const code = 'function hello(
                                        ) {console.log("hello");}';
                                    const analysis = await ai.analyze(
                                        code);
                                    console.assert(analysis.structure,
                                        'Analyze failed');

                                    console.log(
                                        'All Node.js CLI tests passed!');
}

                                    runTests(
                                        ).catch(console.error);
                                    """

                                    with tempfile.NamedTemporaryFile(
                                        mode="w", suffix=".js", delete=False
                                    ) as f:
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

                                            assert (
                                                "All Node.js CLI tests passed!"
                                                in result.stdout
                                            )
                                        finally:
                                            os.unlink(temp_path)

                                            def test_cli_interoperability(self) -> None:
                                                """Test that both CLIs produce compatible results."""
                                                # Create test data with Python CLI
                                                python_script = """
                                                sys.path.insert(0,
                                                    "think-ai-cli/python")

                                                cli = ThinkAICLI(
                                                    )
                                                cli.add("Interoperability test",
                                                    {"lang": "both"})
                                                results = cli.search("interoperability",
                                                    k=1)
                                                print(
                                                    json.dumps(results))
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

                                                python_results = json.loads(
                                                    result.stdout
                                                )
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
                                                    sys.path.insert(0,
                                                        "think-ai-cli/python")
                                                    from think_ai_cli import ThinkAICLI

                                                    cli = ThinkAICLI(
                                                        )

                                                    # Add items
                                                    start = time.time(
                                                        )
for i in range(100):
    cli.add(f"Item {i}", {"index": i})
    add_time = time.time() - start

    # Search items
    start = time.time()
for i in range(20):
    cli.search(f"Item {i}", k=5)
    search_time = time.time() - start

    print(
        f"Python CLI - Add rate: {100/add_time: .2f} items/sec")
    print(
        f"Python CLI - Search rate: {20/search_time: .2f} queries/sec")
    """

    result = subprocess.run(
        [sys.executable, "-c", python_script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
