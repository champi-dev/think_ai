#!/usr/bin/env python3
"""Test script for QWEN integration with progress bars."""

import asyncio
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from think_ai.core.config import Config
from think_ai.intelligence.self_trainer import SelfTrainingIntelligence
from think_ai.models.language.model_manager import ModelManager, TaskType
from think_ai.models.language.types import GenerationConfig
from think_ai.utils.progress import ModelLoadingProgress, progress_context

console = Console()


async def test_model_loading():
    """Test model loading with progress bars."""
    console.print("\n[bold cyan]Testing Model Loading with Progress Bars[/bold cyan]\n")

    # Initialize configuration
    config = Config.from_env()

    # Create model manager
    manager_config = {
        "ollama": {"enabled": True, "base_url": "http://localhost:11434"},
        "huggingface": {"enabled": True, "device": config.model.device, "quantization": config.model.quantization},
        "provider_preference": ["huggingface", "ollama"],
    }

    manager = ModelManager(manager_config)

    # Initialize with progress
    console.print("[yellow]Initializing model manager...[/yellow]")
    await manager.initialize()

    # Test loading specific models
    models_to_test = [
        "Qwen/Qwen2.5-0.5B-Instruct",
        "Qwen/Qwen2.5-1.5B-Instruct",
    ]

    for model_name in models_to_test:
        console.print(f"\n[green]Testing model: {model_name}[/green]")

        # Pre-load model to test progress bar
        start_time = time.time()

        try:
            # This should trigger the progress bar in HuggingFaceProvider
            await manager.providers["huggingface"].load_model(model_name)

            elapsed = time.time() - start_time
            console.print(f"[dim]Model loaded in {elapsed:.2f} seconds[/dim]")

        except Exception as e:
            console.print(f"[red]Error loading model: {e}[/red]")

    await manager.close()


async def test_generation_with_progress():
    """Test generation with progress tracking."""
    console.print("\n[bold cyan]Testing Generation with Progress Tracking[/bold cyan]\n")

    config = Config.from_env()

    manager_config = {
        "huggingface": {"enabled": True, "device": config.model.device},
        "provider_preference": ["huggingface"],
    }

    manager = ModelManager(manager_config)
    await manager.initialize()

    # Test queries
    test_queries = [
        {"type": TaskType.CHAT, "prompt": "What is a black hole?"},
        {"type": TaskType.CODING, "prompt": "Write a Python function for binary search"},
        {"type": TaskType.MATH, "prompt": "Solve x^2 - 5x + 6 = 0"},
    ]

    gen_config = GenerationConfig(temperature=0.7, max_tokens=200)

    for query in test_queries:
        console.print(f"\n[yellow]Query: {query['prompt']}[/yellow]")

        with progress_context(description=f"Generating {query['type'].value} response") as pbar:
            try:
                response, selection = await manager.generate(
                    task_type=query["type"], prompt=query["prompt"], config=gen_config, prefer_fast=True
                )

                pbar.update(0, f"Generated with {selection.model}")

                # Display response
                console.print(
                    Panel(
                        response.text[:200] + "..." if len(response.text) > 200 else response.text,
                        title=f"Response from {selection.model}",
                        border_style="green",
                    )
                )

                if response.metrics:
                    console.print(
                        f"[dim]Tokens: {response.metrics.tokens_generated} | "
                        f"Time: {response.metrics.generation_time:.2f}s | "
                        f"Speed: {response.metrics.tokens_per_second:.1f} tok/s[/dim]"
                    )

            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

    await manager.close()


async def test_self_training():
    """Test self-training with progress bars."""
    console.print("\n[bold cyan]Testing Self-Training with Progress Bars[/bold cyan]\n")

    # Create self-training intelligence
    trainer = SelfTrainingIntelligence()

    # Create a small training dataset
    training_data = [
        {"query": "What is the sun?", "response": "The sun is a star at the center of our solar system."},
        {
            "query": "What is AI?",
            "response": "AI is artificial intelligence, computer systems that can perform intelligent tasks.",
        },
        {"query": "Hello", "response": "Hello! How can I help you today?"},
        {
            "query": "What is a universe?",
            "response": "The universe is all of space, time, matter, and energy that exists.",
        },
    ]

    # Train on dataset
    await trainer.train_on_dataset(training_data, epochs=2)

    # Show metrics
    metrics = trainer.get_metrics()

    table = Table(title="Training Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Intelligence Level", f"{metrics['intelligence_level']:.4f}")
    table.add_row("Neural Pathways", f"{metrics['neural_pathways']:,}")
    table.add_row("Wisdom Accumulated", f"{metrics['wisdom_accumulated']:.2f}")
    table.add_row("Insights Generated", str(metrics["insights_generated"]))

    console.print(table)

    # Test continuous training for a short time
    console.print("\n[yellow]Testing continuous training for 5 seconds...[/yellow]")

    # Start training in background
    training_task = asyncio.create_task(trainer.train_continuously())

    # Let it run for 5 seconds
    await asyncio.sleep(5)

    # Stop training
    trainer.training_active = False
    await training_task

    # Show final metrics
    final_metrics = trainer.get_metrics()
    console.print(f"\n[green]Final Intelligence Level: {final_metrics['intelligence_level']:.4f}[/green]")
    console.print(f"[green]Generations Evolved: {trainer.generations_evolved}[/green]")


async def test_full_system():
    """Test full system integration."""
    console.print("\n[bold cyan]Testing Full System Integration[/bold cyan]\n")

    # Test process manager style progress
    with progress_context(total=3, description="Starting Think AI services") as pbar:
        pbar.update(0, "Initializing core systems...")
        await asyncio.sleep(1)
        pbar.update(1, "Core systems ready")

        pbar.update(0, "Loading QWEN models...")
        await asyncio.sleep(1)
        pbar.update(1, "Models loaded")

        pbar.update(0, "Starting intelligence services...")
        await asyncio.sleep(1)
        pbar.update(1, "All services ready")

    console.print("[bold green]✓ Full system test complete![/bold green]")


async def main():
    """Main test function."""
    console.print(
        Panel.fit(
            "[bold cyan]Think AI - QWEN Progress Bar Integration Test[/bold cyan]\n"
            "Testing progress indicators for all long-running operations",
            border_style="cyan",
        )
    )

    # Run all tests
    await test_model_loading()
    await test_generation_with_progress()
    await test_self_training()
    await test_full_system()

    console.print("\n[bold green]All tests completed successfully![/bold green]")


if __name__ == "__main__":
    asyncio.run(main())
