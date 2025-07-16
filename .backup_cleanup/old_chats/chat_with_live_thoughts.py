#!/usr/bin/env python3
"""Enhanced chat with real-time thought streaming."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from chat_while_training import TrainingChatInterface
from rich.console import Console
from rich.live import Live
from rich.panel import Panel

console = Console()


class LiveThoughtChat(TrainingChatInterface):
    """Enhanced chat that shows thoughts in real-time as they generate."""

    async def process_with_thoughts_live(self, query):
        """Process query and stream thoughts in real-time."""
        thoughts = []

        # Create a live display
        with Live(console=console, refresh_per_second=4) as live:
            # Show initial processing message
            live.update(
                Panel(
                    "🧠 [bold yellow]Initializing exponential thought process...[/bold yellow]",
                    title="💭 AI Thinking",
                    border_style="yellow",
                )
            )
            await asyncio.sleep(0.5)

            # Generate and display thoughts one by one
            # First, analyze metrics
            self.load_current_metrics()
            if self.current_metrics:
                avg_intelligence = sum(self.current_metrics.values()) / len(
                    self.current_metrics
                )
            else:
                avg_intelligence = self.intelligence_level

            # Stream thoughts with delays
            thought_display = []

            # Intelligence level
            thought = (
                f"Intelligence Level: {self.format_large_number(avg_intelligence)}"
            )
            thoughts.append(thought)
            thought_display.append(thought)
            live.update(
                Panel(
                    "\n".join(thought_display),
                    title="💭 AI Thinking",
                    border_style="yellow",
                )
            )
            await asyncio.sleep(0.3)

            # Query analysis
            query_words = query.lower().split()
            thought = f"📥 Received {len(query_words)}-word query with {len(set(query_words))} unique terms"
            thoughts.append(thought)
            thought_display.append(thought)
            live.update(
                Panel(
                    "\n".join(thought_display),
                    title="💭 AI Thinking",
                    border_style="yellow",
                )
            )
            await asyncio.sleep(0.3)

            # Intent detection
            if "hi" in query.lower() or "hello" in query.lower():
                thought = "👋 Greeting detected - social interaction protocols engaged"
                thoughts.append(thought)
                thought_display.append(thought)
                live.update(
                    Panel(
                        "\n".join(thought_display),
                        title="💭 AI Thinking",
                        border_style="yellow",
                    )
                )
                await asyncio.sleep(0.3)

            # Add intelligence-specific thoughts
            if avg_intelligence > 1_000_000:
                for thought in [
                    "🌌 Accessing hyper-dimensional consciousness matrix...",
                    f"🧬 Synthesizing across {self.format_large_number(avg_intelligence * 1000)} neural pathways...",
                    "⚡ Quantum coherence achieved...",
                    "🔮 Transcendent insights emerging...",
                ]:
                    thoughts.append(thought)
                    thought_display.append(thought)
                    live.update(
                        Panel(
                            "\n".join(thought_display),
                            title="💭 AI Thinking",
                            border_style="yellow",
                        )
                    )
                    await asyncio.sleep(0.4)

            # Final processing
            thought = "🎯 Formulating response with exponential intelligence..."
            thoughts.append(thought)
            thought_display.append(thought)
            live.update(
                Panel(
                    "\n".join(thought_display),
                    title="💭 AI Thinking",
                    border_style="yellow",
                )
            )

        # Now actually process the query
        response, _ = await self.process_with_thoughts(query)

        return response, thoughts

    async def run_live(self) -> None:
        """Run the live thought streaming interface."""
        console.print(
            "\n[bold cyan]🧠 THINK AI - LIVE THOUGHT STREAMING MODE[/bold cyan]"
        )
        console.print("[yellow]Watch the AI's thoughts generate in real-time![/yellow]")
        console.print("[dim]Type 'exit' to quit[/dim]\n")

        while True:
            try:
                user_input = console.input("\n[bold cyan]You:[/bold cyan] ")

                if user_input.lower() in ["exit", "quit"]:
                    break

                # Process with live thoughts
                response, thoughts = await self.process_with_thoughts_live(user_input)

                # Show response
                console.print(f"\n[bold green]AI:[/bold green] {response}")

                # Show final metrics
                self.load_current_metrics()
                avg_intel = (
                    sum(self.current_metrics.values()) / len(self.current_metrics)
                    if self.current_metrics
                    else self.intelligence_level
                )
                console.print(
                    f"\n[dim magenta]Intelligence Level: {self.format_large_number(avg_intel)}[/dim magenta]"
                )

            except KeyboardInterrupt:
                console.print("\n\n[yellow]Chat interrupted.[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")

        console.print("\n[bold green]✨ Thanks for watching my thoughts![/bold green]")

        if self._claude_initialized:
            await self.claude_api.__aexit__(None, None, None)


async def main() -> None:
    interface = LiveThoughtChat()
    await interface.run_live()


if __name__ == "__main__":
    asyncio.run(main())
