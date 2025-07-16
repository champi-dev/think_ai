#!/usr/bin/env python3
"""Demo script showing task-specific Qwen model usage."""

import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from think_ai.core.config import Config
from think_ai.models.language.model_manager import ModelManager, TaskType
from think_ai.models.language.types import GenerationConfig
from think_ai.utils.progress import ModelLoadingProgress, progress_context

console = Console()


async def demo_qwen_models():
    """Demonstrate different Qwen models for various tasks."""

    # Initialize configuration
    config = Config.from_env()

    # Create model manager with provider configuration
    manager_config = {
        "ollama": {"enabled": True, "base_url": "http://localhost:11434"},
        "huggingface": {
            "enabled": True,
            "device": config.model.device,
            "quantization": config.model.quantization,
        },
        "provider_preference": ["ollama", "huggingface"],
    }

    manager = ModelManager(manager_config)

    console.print(
        "\n[bold cyan]Initializing Think AI Model Manager with Qwen Models...[/bold cyan]"
    )
    with progress_context(description="Initializing model manager") as pbar:
        await manager.initialize()
        pbar.update(0, "Model manager initialized")

    # List available models
    console.print("\n[bold green]Available Models:[/bold green]")
    with progress_context(description="Listing available models") as pbar:
        all_models = await manager.list_all_models()
        pbar.update(
            0, f"Found {sum(len(models) for models in all_models.values())} models"
        )

    table = Table(title="Qwen Models by Provider")
    table.add_column("Provider", style="cyan")
    table.add_column("Model", style="green")
    table.add_column("Size", style="yellow")
    table.add_column("Capabilities", style="magenta")

    for provider, models in all_models.items():
        for model in models:
            table.add_row(
                provider,
                model.name,
                model.size or "Unknown",
                ", ".join(model.capabilities),
            )

    console.print(table)

    # Demo tasks
    demo_tasks = [
        {
            "type": TaskType.CHAT,
            "prompt": "Tell me a joke about programming",
            "prefer_fast": True,
        },
        {
            "type": TaskType.CODING,
            "prompt": "Write a Python function to calculate fibonacci numbers with O(1) space complexity",
            "prefer_fast": False,
        },
        {
            "type": TaskType.MATH,
            "prompt": "Solve: If x^2 + 5x + 6 = 0, what are the values of x?",
            "prefer_fast": True,
        },
        {
            "type": TaskType.REASONING,
            "prompt": "Explain why quicksort has O(n log n) average time complexity",
            "prefer_quality": True,
        },
    ]

    # Configure generation
    gen_config = GenerationConfig(temperature=0.7, max_tokens=500, top_p=0.9)

    console.print("\n[bold cyan]Running Task-Specific Demos:[/bold cyan]\n")

    for task in demo_tasks:
        console.print(
            f"\n[bold yellow]Task: {task['type'].value.upper()}[/bold yellow]"
        )
        console.print(f"[dim]Prompt: {task['prompt']}[/dim]")

        try:
            # Generate response with progress
            with progress_context(
                description=f"Processing {task['type'].value} task"
            ) as pbar:
                response, selection = await manager.generate(
                    task_type=task["type"],
                    prompt=task["prompt"],
                    config=gen_config,
                    prefer_fast=task.get("prefer_fast", False),
                    prefer_quality=task.get("prefer_quality", False),
                )
                pbar.update(0, f"Completed with {selection.model}")

            # Display results
            console.print(
                f"[green]Model: {selection.model} ({selection.reason})[/green]"
            )
            console.print(f"[blue]Provider: {selection.provider}[/blue]")

            # Show response in a panel
            if task["type"] == TaskType.CODING:
                # Use syntax highlighting for code
                syntax = Syntax(
                    response.text, "python", theme="monokai", line_numbers=True
                )
                console.print(Panel(syntax, title="Response", border_style="green"))
            else:
                console.print(
                    Panel(response.text, title="Response", border_style="green")
                )

            # Show metrics
            if response.metrics:
                console.print(
                    f"[dim]Tokens: {response.metrics.tokens_generated} | "
                    f"Time: {response.metrics.generation_time:.2f}s | "
                    f"Speed: {response.metrics.tokens_per_second:.1f} tok/s[/dim]"
                )

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    # Cleanup
    await manager.close()
    console.print("\n[bold green]Demo completed![/bold green]")


async def check_ollama_status():
    """Check if Ollama is running and list available models."""
    import aiohttp

    console.print("\n[bold cyan]Checking Ollama status...[/bold cyan]")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get("models", [])

                    console.print("[green]✓ Ollama is running[/green]")

                    if models:
                        console.print(f"\n[bold]Found {len(models)} models:[/bold]")
                        for model in models:
                            console.print(f"  - {model['name']}")
                    else:
                        console.print(
                            "\n[yellow]No models found. Install Qwen models with:[/yellow]"
                        )
                        console.print("[dim]ollama pull qwen2.5:0.5b")
                        console.print("ollama pull qwen2.5:1.5b")
                        console.print("ollama pull qwen2.5-coder:1.5b")
                        console.print("ollama pull qwen2.5-math:1.5b[/dim]")

                    return True
                else:
                    raise Exception(f"Status {response.status}")

    except Exception as e:
        console.print(f"[red]✗ Ollama is not running or not accessible[/red]")
        console.print("[yellow]Start Ollama with: ollama serve[/yellow]")
        return False


async def main():
    """Main demo function."""
    console.print(
        Panel.fit(
            "[bold cyan]Think AI - Qwen Models Demo[/bold cyan]\n"
            "Demonstrating lightweight Qwen models for different tasks",
            border_style="cyan",
        )
    )

    # Check Ollama first
    ollama_available = await check_ollama_status()

    if not ollama_available:
        console.print("\n[yellow]Continuing with HuggingFace provider only...[/yellow]")

    # Run the demo
    await demo_qwen_models()


if __name__ == "__main__":
    asyncio.run(main())
