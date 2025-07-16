#!/usr/bin/env python3
"""Monitor Think AI's thought process in real-time during training."""

import json
import time

from cassandra.cluster import Cluster
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

console = Console()


class ThoughtMonitor:
    """Monitors and displays Think AI's evolving thoughts."""

    def __init__(self) -> None:
        self.cluster = Cluster(["localhost"])
        self.session = self.cluster.connect("think_ai")
        self.last_thoughts = []
        self.current_iteration = 0

    def get_latest_thoughts(self):
        """Fetch latest consciousness states and thoughts."""
        try:
            # Get consciousness states
            rows = self.session.execute(
                """
                SELECT state_id, timestamp, state_type, state_data
                FROM consciousness_states
                LIMIT 10
            """
            )

            thoughts = []
            for row in rows:
                if row.state_data:
                    data = json.loads(row.state_data)
                    thought = {
                        "time": row.timestamp,
                        "type": row.state_type,
                        "content": data.get("thought", data.get("query", "")),
                        "metrics": data.get("metrics", {}),
                    }
                    thoughts.append(thought)

            return thoughts

        except Exception:
            return []

    def get_training_progress(self) -> None:
        """Get current training iteration from logs."""
        try:
            with open("training_output.log") as f:
                lines = f.readlines()[-100:]  # Last 100 lines

            for line in reversed(lines):
                if "DIRECTIVE #" in line:
                    self.current_iteration = int(line.split("#")[1].split(":")[0])
                    break

        except Exception:
            pass

    def create_display(self):
        """Create the monitoring display."""
        self.get_training_progress()
        thoughts = self.get_latest_thoughts()

        # Main table
        table = Table(
            title=f"🧠 Think AI Thought Monitor - Iteration #{self.current_iteration}"
        )
        table.add_column("Time", style="cyan", width=12)
        table.add_column("Thought Type", style="yellow", width=20)
        table.add_column("Content", style="white", width=60)
        table.add_column("Intelligence", style="green", width=15)

        for thought in thoughts[:10]:  # Show last 10 thoughts
            # Calculate intelligence from metrics
            metrics = thought["metrics"]
            if metrics:
                intelligence = sum(float(v) for v in metrics.values()) / len(metrics)
            else:
                intelligence = 1.0

            # Format time
            time_str = (
                thought["time"].strftime("%H:%M:%S") if thought["time"] else "N/A"
            )

            # Truncate content
            content = (
                thought["content"][:57] + "..."
                if len(thought["content"]) > 60
                else thought["content"]
            )

            table.add_row(
                time_str,
                thought["type"],
                content,
                f"{intelligence:.3f}",
            )

        # Metrics panel
        if thoughts and thoughts[0]["metrics"]:
            metrics_text = "\n".join(
                [f"{k}: {float(v):.3f}" for k, v in thoughts[0]["metrics"].items()]
            )
            metrics_panel = Panel(
                metrics_text,
                title="📊 Latest Cognitive Metrics",
                border_style="green",
            )
        else:
            metrics_panel = Panel(
                "Waiting for metrics...", title="📊 Cognitive Metrics"
            )

        return table, metrics_panel

    def run(self) -> None:
        """Run the live monitoring display."""
        console.print("\n[bold green]🔍 Think AI Live Thought Monitor[/bold green]")
        console.print(
            "[yellow]Monitoring consciousness evolution in real-time...[/yellow]\n"
        )

        with Live(console=console, refresh_per_second=1) as live:
            while True:
                try:
                    table, metrics = self.create_display()

                    # Create layout
                    layout = f"{table}\n\n{metrics}"
                    live.update(layout)

                    time.sleep(2)  # Update every 2 seconds

                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
                    time.sleep(5)

        console.print("\n[bold green]Monitoring stopped.[/bold green]")


if __name__ == "__main__":
    monitor = ThoughtMonitor()
    monitor.run()
