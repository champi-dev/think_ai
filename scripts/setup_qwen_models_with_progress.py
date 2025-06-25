#!/usr/bin/env python3
"""Setup script for Qwen models with progress tracking."""

import asyncio
import subprocess
import sys

import aiohttp
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from think_ai.utils.progress import O1ProgressBar, progress_context

console = Console()


async def check_ollama_installed():
    """Check if Ollama is installed."""
    try:
        result = subprocess.run(["which", "ollama"], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


async def check_ollama_running():
    """Check if Ollama service is running."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://localhost:11434/api/tags", timeout=aiohttp.ClientTimeout(total=2)
            ) as response:
                return response.status == 200
    except:
        return False


async def start_ollama():
    """Start Ollama service."""
    console.print("[yellow]Starting Ollama service...[/yellow]")
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for service to start
    with progress_context(description="Waiting for Ollama to start") as pbar:
        for i in range(10):
            if await check_ollama_running():
                pbar.update(0, "Ollama started successfully")
                return True
            await asyncio.sleep(1)
            pbar.update(0, f"Waiting... ({i+1}/10)")

    return False


async def pull_model(model_name: str, description: str):
    """Pull a model with progress tracking."""
    console.print(f"\n[cyan]Installing {model_name}[/cyan] - {description}")

    # Create progress bar
    pbar = O1ProgressBar(description=f"Downloading {model_name}")

    # Start the pull process
    process = await asyncio.create_subprocess_exec(
        "ollama", "pull", model_name, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    # Monitor output
    while True:
        line = await process.stdout.readline()
        if not line:
            break

        # Parse progress from ollama output
        line_text = line.decode().strip()
        if line_text:
            # Update progress bar with ollama output
            pbar.update(0, line_text[:50])  # Truncate long lines

    # Wait for completion
    await process.wait()

    if process.returncode == 0:
        pbar.finish(f"✓ {model_name} installed successfully")
    else:
        pbar.finish(f"✗ Failed to install {model_name}")
        stderr = await process.stderr.read()
        console.print(f"[red]Error: {stderr.decode()}[/red]")


async def list_installed_models():
    """List installed Qwen models."""
    console.print("\n[bold cyan]Checking installed models...[/bold cyan]")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get("models", [])

                    # Filter Qwen models
                    qwen_models = [m for m in models if "qwen" in m["name"].lower()]

                    if qwen_models:
                        table = Table(title="Installed Qwen Models")
                        table.add_column("Model", style="cyan")
                        table.add_column("Size", style="yellow")
                        table.add_column("Modified", style="green")

                        for model in qwen_models:
                            size_gb = model.get("size", 0) / (1024**3)
                            table.add_row(model["name"], f"{size_gb:.1f} GB", model.get("modified_at", "Unknown")[:10])

                        console.print(table)
                    else:
                        console.print("[yellow]No Qwen models installed yet[/yellow]")

                    return qwen_models
    except Exception as e:
        console.print(f"[red]Error listing models: {e}[/red]")
        return []


async def main():
    """Main setup function."""
    console.print(
        Panel.fit(
            "[bold cyan]Think AI - Qwen Models Setup[/bold cyan]\n"
            "Installing lightweight models with progress tracking",
            border_style="cyan",
        )
    )

    # Check prerequisites
    with progress_context(total=2, description="Checking prerequisites") as pbar:
        # Check Ollama installation
        if not await check_ollama_installed():
            pbar.finish("✗ Ollama not installed")
            console.print("\n[red]❌ Ollama is not installed.[/red]")
            console.print("Please install Ollama from: https://ollama.com/download")
            sys.exit(1)

        pbar.update(1, "Ollama installed")

        # Check if Ollama is running
        if not await check_ollama_running():
            pbar.update(0, "Starting Ollama service...")
            if not await start_ollama():
                pbar.finish("✗ Failed to start Ollama")
                console.print("[red]Failed to start Ollama service[/red]")
                sys.exit(1)

        pbar.update(1, "Ollama service running")

    # Define models to install
    minimal_models = [
        ("qwen2.5:0.5b", "Ultra-fast chat (0.5B parameters)"),
        ("qwen2.5:1.5b", "Fast general chat (1.5B parameters)"),
        ("qwen2.5-coder:1.5b", "Fast code generation (1.5B parameters)"),
    ]

    balanced_models = [
        ("qwen2.5:3b", "Better chat quality (3B parameters)"),
        ("qwen2.5-coder:7b", "Excellent code generation (7B parameters)"),
        ("qwen2.5-math:1.5b", "Math problem solving (1.5B parameters)"),
    ]

    # Install minimal models
    console.print("\n[bold]1️⃣  Installing Minimal Setup (Ultra Fast)[/bold]")
    console.print("[dim]These models provide fast responses with minimal resource usage[/dim]\n")

    for model, desc in minimal_models:
        await pull_model(model, desc)

    # Show optional models
    console.print("\n[bold]2️⃣  Optional: Balanced Setup (Better Quality)[/bold]")
    console.print("[dim]For better quality responses, you can also install:[/dim]")
    for model, desc in balanced_models:
        console.print(f"  ollama pull {model}  # {desc}")

    console.print("\n[bold]3️⃣  Optional: Quality Setup (Best Results)[/bold]")
    console.print("[dim]For best quality (requires more resources):[/dim]")
    console.print("  ollama pull qwen2.5:7b          # High quality chat")
    console.print("  ollama pull qwen2.5-coder:32b   # Production-grade code")
    console.print("  ollama pull qwen2.5-math:7b     # Advanced mathematics")
    console.print("  ollama pull qwenvl2:7b          # Multimodal (vision+text)")

    # List installed models
    await list_installed_models()

    console.print("\n[bold green]✅ Setup complete![/bold green]")
    console.print("\nTo test the models, run:")
    console.print("  [cyan]python examples/qwen_models_demo.py[/cyan]")
    console.print("\nTo use a specific model with Ollama:")
    console.print("  [cyan]ollama run qwen2.5:0.5b[/cyan]")


if __name__ == "__main__":
    asyncio.run(main())
