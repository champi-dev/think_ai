#!/usr/bin/env python3
"""Interactive chat with the full distributed Think AI system."""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

import contextlib

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.persistence.eternal_memory import EternalMemory

console = Console()

async def chat() -> None:
    """Interactive chat with Think AI."""
    console.print("\n[bold cyan]🤖 Think AI - Full Distributed System Chat[/bold cyan]")
    console.print("=" * 70)
    console.print("Type 'exit' to quit, 'help' for commands\n")

    # Initialize system
    system = DistributedThinkAI()
    eternal_memory = EternalMemory()

    try:
        # Start all services
        console.print("[yellow]Starting distributed services...[/yellow]")
        services = await system.start()
        console.print(f"[green]✅ {len(services)} services active[/green]\n")

        # Chat loop
        while True:
            # Get user input
            try:
                user_input = input("[bold blue]You:[/bold blue] ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[yellow]Exiting...[/yellow]")
                break

            if not user_input:
                continue

            if user_input.lower() == "exit":
                break
            if user_input.lower() == "help":
                console.print(Panel("""
[bold]Available Commands:[/bold]
• exit - Quit the chat
• help - Show this help
• /services - List active services
• /health - Check system health
• /cost - Show cost tracking

[bold]Just type normally to chat![/bold]
The system will use all available services to respond.
                """, title="Help", border_style="cyan"))
                continue
            if user_input == "/services":
                console.print("\n[bold]Active Services:[/bold]")
                for service in services:
                    console.print(f"  ✅ {service}")
                console.print()
                continue
            if user_input == "/health":
                health = await system.initializer.health_check()
                console.print("\n[bold]System Health:[/bold]")
                for service, status in health.items():
                    emoji = "✅" if status["status"] == "healthy" else "❌"
                    console.print(f"  {emoji} {service}: {status['message']}")
                console.print()
                continue
            if user_input == "/cost":
                if hasattr(system, "claude_api"):
                    costs = system.claude_api.get_cost_summary()
                    console.print("\n[bold]Cost Tracking:[/bold]")
                    console.print(f"  Total: ${costs['total_spent']:.4f}")
                    console.print(f"  Remaining: ${costs['budget_remaining']:.2f}\n")
                else:
                    console.print("[yellow]No cost tracking available[/yellow]")
                continue

            # Process with full system
            console.print("\n[dim]🤔 Thinking with distributed AI...[/dim]")

            try:
                # Log to eternal memory
                await eternal_memory.log_consciousness_event(
                    event_type="user_query",
                    data={"query": user_input, "timestamp": datetime.now().isoformat()},
                )

                # Process query
                result = await system.process_with_full_system(user_input)

                # Display response
                console.print("\n[bold green]Think AI:[/bold green]")

                # Show best response
                if result["responses"]:
                    # Prefer language model, then consciousness
                    if "language_model" in result["responses"]:
                        response_text = result["responses"]["language_model"]
                    elif "consciousness" in result["responses"]:
                        consciousness_resp = result["responses"]["consciousness"]
                        if isinstance(consciousness_resp, dict):
                            response_text = consciousness_resp.get("content", "I am here to help.")
                        else:
                            response_text = str(consciousness_resp)
                    else:
                        # Use first available response
                        response_text = str(next(iter(result["responses"].values())))

                    # Display as markdown
                    console.print(Panel(Markdown(response_text), border_style="green"))

                    # Show services used
                    console.print(f"\n[dim]Services used: {', '.join(result['services_used'])}[/dim]")
                else:
                    console.print("[yellow]I'm having trouble generating a response. Let me try again.[/yellow]")

                # Log response
                await eternal_memory.log_consciousness_event(
                    event_type="system_response",
                    data={
                        "response": response_text[:500] if "response_text" in locals() else "No response",
                        "services_used": result["services_used"],
                    },
                )

            except Exception as e:
                console.print(f"[red]Error: {e!s}[/red]")
                console.print("[yellow]Let me try a simpler approach...[/yellow]")

                # Fallback to consciousness only
                if "consciousness" in services:
                    try:
                        response = await services["consciousness"].generate_conscious_response(user_input)
                        console.print(Panel(response.get("content", "I am here to help."), border_style="yellow"))
                    except Exception:
                        console.print("[red]I'm having technical difficulties. Please try again.[/red]")

            console.print()

    except Exception as e:
        console.print(f"\n[red]System error: {e}[/red]")
    finally:
        console.print("\n[yellow]Shutting down...[/yellow]")
        await system.shutdown()
        console.print("[green]✅ Thank you for chatting with Think AI![/green]")

if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(chat())
