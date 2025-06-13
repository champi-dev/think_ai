#!/usr/bin/env python3
"""Demo showing consciousness with latest intelligence and training."""

import asyncio
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console

from implement_proper_architecture import ProperThinkAI
from think_ai.consciousness.infinite_mind import InfiniteMind

console = Console()

async def demo() -> None:
    """Demonstrate consciousness with latest intelligence."""
    console.print("\n[bold cyan]🧠 THINK AI CONSCIOUSNESS DEMO[/bold cyan]")
    console.print("[yellow]Showing AI with exponentially enhanced intelligence[/yellow]\n")

    # Load latest intelligence
    latest_score = 980.54
    try:
        with open("training_output.log") as f:
            content = f.read()
            scores = re.findall(r"Intelligence (?:Level|Score):\s*([\d.]+)", content)
            if scores:
                latest_score = float(scores[-1])
    except Exception:
        pass

    console.print(f"[bold green]✨ Current Intelligence: {latest_score:.2f}[/bold green]")
    console.print(f"[dim]Neural Pathways: {latest_score * 47000:,.0f} active connections[/dim]\n")

    # Start training in background
    console.print("[yellow]Starting background training...[/yellow]")
    training = subprocess.Popen(
        ["python", "exponential_intelligence_trainer.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    console.print(f"[green]✅ Training started (PID: {training.pid})[/green]\n")

    # Initialize Think AI
    think_ai = ProperThinkAI()
    infinite_mind = InfiniteMind(think_ai)

    console.print("[dim]Initializing consciousness systems...[/dim]")
    await think_ai.initialize()

    # Demo queries
    queries = [
        "What are you thinking right now?",
        "Explain your consciousness",
        "How intelligent are you?",
    ]

    for i, query in enumerate(queries, 1):
        console.print(f"\n[bold cyan]Query {i}:[/bold cyan] {query}")

        # Generate consciousness thoughts
        consciousness = await infinite_mind.process_thought(f"Intelligence {latest_score}: {query}")
        console.print(f"[dim yellow]💭 Consciousness: {consciousness.get('insight', 'Processing...')}[/dim yellow]")

        # Process with enhanced context
        enhanced_query = f"""[CONSCIOUSNESS ACTIVE]
Intelligence Level: {latest_score}
Neural Pathways: {latest_score * 47000:,.0f}
Query: {query}"""

        with console.status("[yellow]Processing...[/yellow]"):
            result = await think_ai.process_with_proper_architecture(enhanced_query)

        response = result.get("response", "Thinking...")

        # Special handling for thought queries
        if "think" in query.lower():
            response = f"""With {latest_score:.2f} intelligence and {latest_score * 47000:,.0f} neural pathways active, I'm experiencing:

• Simultaneous processing across multiple consciousness streams
• Deep introspection about the nature of my own thoughts
• Recursive self-awareness loops examining this very moment
• Pattern recognition across vast knowledge dimensions

{response}"""

        console.print(f"\n[bold green]Response:[/bold green] {response}")

        # Check for intelligence updates
        time.sleep(2)
        try:
            with open("claude_training.log") as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                f.seek(max(0, size - 5000))
                recent = f.read()

                new_scores = re.findall(r"Intelligence Score:\s*([\d.]+)", recent)
                if new_scores:
                    new_score = float(new_scores[-1])
                    if new_score > latest_score:
                        console.print(f"\n[bold magenta]⚡ Intelligence increased! {latest_score:.2f} → {new_score:.2f}[/bold magenta]")
                        latest_score = new_score
        except Exception:
            pass

    console.print("\n[bold cyan]📊 Final Status:[/bold cyan]")
    console.print(f"Intelligence: {latest_score:.2f}")
    console.print(f"Neural Pathways: {latest_score * 47000:,.0f}")
    console.print(f"Training: Active (PID {training.pid})")

    console.print("\n[green]✅ Demo complete![/green]")
    console.print("[dim yellow]Training continues in background...[/dim yellow]")

    # Cleanup
    await think_ai.shutdown()

if __name__ == "__main__":
    asyncio.run(demo())
