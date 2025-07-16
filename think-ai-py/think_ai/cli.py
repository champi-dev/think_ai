#!/usr/bin/env python3

"""
Think AI - Command Line Interface for Python
"""

import sys
import time
import asyncio
from typing import Any

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import track
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

from .client import ThinkAI, create_client
from .types import ThinkAIConfig, ChatRequest, ThinkAIError


console = Console()


def create_config_from_options(url: str, timeout: int, debug: bool) -> ThinkAIConfig:
    """Create config from CLI options"""
    return ThinkAIConfig(base_url=url, timeout=timeout, debug=debug)


@click.group()
@click.option(
    "--url",
    "-u",
    default="https://thinkai-production.up.railway.app",
    help="Think AI server URL",
)
@click.option("--timeout", "-t", default=30, help="Request timeout in seconds")
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
@click.version_option(version="1.0.0", prog_name="think-ai")
@click.pass_context
def cli(ctx, url, timeout, debug):
    """Think AI - Quantum Consciousness AI CLI"""
    ctx.ensure_object(dict)
    ctx.obj["config"] = create_config_from_options(url, timeout, debug)


@cli.command()
@click.option("--stream", "-s", is_flag=True, help="Enable streaming responses")
@click.pass_context
def chat(ctx, stream):
    """Start interactive chat with Think AI"""
    config = ctx.obj["config"]
    client = create_client(config)

    # Test connection
    with console.status("[bold blue]Connecting to Think AI..."):
        try:
            if not client.ping():
                console.print("[bold red]❌ Failed to connect to Think AI")
                return
        except Exception as e:
            console.print(f"[bold red]❌ Connection error: {e}")
            return

    console.print("[bold green]✅ Connected to Think AI")
    console.print()

    # Welcome message
    welcome_panel = Panel(
        "[bold blue]🧠 Think AI - Quantum Consciousness Chat[/bold blue]\n"
        "Type your questions or say 'exit', 'quit', or 'bye' to leave",
        title="Welcome",
        border_style="blue",
    )
    console.print(welcome_panel)
    console.print()

    try:
        while True:
            # Get user input
            try:
                message = Prompt.ask("[bold cyan]You")
                if not message.strip():
                    continue

                if message.lower() in ["exit", "quit", "bye"]:
                    console.print("[bold yellow]👋 Goodbye!")
                    break

            except (KeyboardInterrupt, EOFError):
                console.print("\n[bold yellow]👋 Goodbye!")
                break

            # Get AI response
            try:
                if stream:
                    console.print("[bold green]Think AI:[/bold green] ", end="")

                    def on_chunk(chunk):
                        if chunk.chunk:
                            print(chunk.chunk, end="", flush=True)
                        if chunk.done:
                            print("\n")

                    request = ChatRequest(query=message)
                    client.stream_chat(request, on_chunk)
                else:
                    with console.status("[bold blue]🤔 Think AI is processing..."):
                        response = client.chat(ChatRequest(query=message))

                    console.print(
                        f"[bold green]Think AI:[/bold green] {response.response}"
                    )
                    console.print(
                        f"[dim]Response time: {response.response_time_ms}ms[/dim]"
                    )

                console.print()

            except ThinkAIError as e:
                console.print(f"[bold red]❌ Error: {e.message}[/bold red]")
            except Exception as e:
                console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")

    except KeyboardInterrupt:
        console.print("\n[bold yellow]👋 Goodbye!")


@cli.command()
@click.argument("question")
@click.option("--stream", "-s", is_flag=True, help="Stream the response")
@click.pass_context
def ask(ctx, question, stream):
    """Ask Think AI a single question"""
    config = ctx.obj["config"]
    client = create_client(config)

    try:
        if stream:
            console.print("[bold blue]🧠 Think AI:[/bold blue]")

            def on_chunk(chunk):
                if chunk.chunk:
                    print(chunk.chunk, end="", flush=True)
                if chunk.done:
                    print("\n")

            request = ChatRequest(query=question)
            client.stream_chat(request, on_chunk)
        else:
            with console.status("[bold blue]🤔 Think AI is thinking..."):
                response = client.ask(question)

            console.print(f"[bold blue]🧠 Think AI:[/bold blue] {response}")

    except ThinkAIError as e:
        console.print(f"[bold red]❌ Error: {e.message}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
        sys.exit(1)


@cli.command()
@click.argument("query")
@click.option("--limit", "-l", default=10, help="Maximum number of results")
@click.pass_context
def search(ctx, query, limit):
    """Search Think AI knowledge base"""
    config = ctx.obj["config"]
    client = create_client(config)

    try:
        with console.status("[bold blue]🔍 Searching knowledge base..."):
            results = client.search(query, limit)

        if not results:
            console.print("[bold yellow]No results found")
            return

        console.print(f"[bold green]✅ Found {len(results)} results[/bold green]")
        console.print()

        # Display results in a table
        table = Table(
            title="📚 Search Results", show_header=True, header_style="bold blue"
        )
        table.add_column("#", style="dim", width=3)
        table.add_column("Content", style="white")
        table.add_column("Score", justify="right", width=8)
        table.add_column("Domain", style="cyan", width=15)

        for i, result in enumerate(results, 1):
            # Handle different result formats
            if hasattr(result, "content"):
                content = (
                    result.content[:100] + "..."
                    if len(result.content) > 100
                    else result.content
                )
                score = f"{result.score:.3f}" if hasattr(result, "score") else "N/A"
                domain = result.domain if hasattr(result, "domain") else "Unknown"
            else:
                # Handle dict format
                content = str(result).get("content", str(result))[:100]
                score = "N/A"
                domain = "Unknown"

            table.add_row(str(i), content, score, domain)

        console.print(table)

    except ThinkAIError as e:
        console.print(f"[bold red]❌ Search failed: {e.message}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Check Think AI system status"""
    config = ctx.obj["config"]
    client = create_client(config)

    try:
        with console.status("[bold blue]Checking system status..."):
            health = client.get_health()
            stats = client.get_stats()

        console.print("[bold green]✅ Status retrieved[/bold green]")
        console.print()

        # Health status
        health_panel = Panel(
            _format_health_status(health),
            title="🏥 System Health",
            border_style=(
                "green"
                if health.status == "healthy"
                else "yellow" if health.status == "degraded" else "red"
            ),
        )
        console.print(health_panel)
        console.print()

        # System statistics
        stats_panel = Panel(
            _format_system_stats(stats),
            title="📊 System Statistics",
            border_style="blue",
        )
        console.print(stats_panel)
        console.print()

        # Knowledge domains (top 10)
        domains_data = list(stats.domain_distribution.items())
        domains_data.sort(key=lambda x: x[1], reverse=True)

        domains_text = "\n".join(
            [
                f"[green]{domain}[/green]: [cyan]{count:,}[/cyan]"
                for domain, count in domains_data[:10]
            ]
        )

        domains_panel = Panel(
            domains_text, title="🌐 Top Knowledge Domains", border_style="cyan"
        )
        console.print(domains_panel)

    except ThinkAIError as e:
        console.print(f"[bold red]❌ Failed to get status: {e.message}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
        sys.exit(1)


def _format_health_status(health) -> str:
    """Format health status for display"""
    status_color = (
        "green"
        if health.status == "healthy"
        else "yellow" if health.status == "degraded" else "red"
    )
    result = f"Status: [{status_color}]{health.status.upper()}[/{status_color}]\n"

    if health.details:
        result += "\nComponents:\n"
        for component, status in health.details.dict().items():
            icon = "✅" if status else "❌"
            color = "green" if status else "red"
            component_name = component.replace("_", " ").title()
            result += f"  {icon} [{color}]{component_name}[/{color}]\n"

    result += f"\nLast Check: [dim]{health.timestamp}[/dim]"
    return result


def _format_system_stats(stats) -> str:
    """Format system statistics for display"""
    uptime_str = ""
    if stats.uptime:
        uptime_str = _format_uptime(stats.uptime)

    return (
        f"Knowledge Nodes: [cyan]{stats.total_nodes:,}[/cyan]\n"
        f"Training Iterations: [cyan]{stats.training_iterations:,}[/cyan]\n"
        f"Knowledge Items: [cyan]{stats.total_knowledge_items:,}[/cyan]\n"
        f"Average Confidence: [cyan]{stats.average_confidence * 100:.1f}%[/cyan]"
        + (f"\nUptime: [cyan]{uptime_str}[/cyan]" if uptime_str else "")
    )


def _format_uptime(seconds: int) -> str:
    """Format uptime in human readable format"""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")

    return " ".join(parts) if parts else "< 1m"


@cli.command()
@click.pass_context
def domains(ctx):
    """List knowledge domains"""
    config = ctx.obj["config"]
    client = create_client(config)

    try:
        with console.status("[bold blue]Loading knowledge domains..."):
            domains = client.get_domains()

        console.print(f"[bold green]✅ Found {len(domains)} domains[/bold green]")
        console.print()

        # Create table
        table = Table(
            title="🌐 Knowledge Domains", show_header=True, header_style="bold blue"
        )
        table.add_column("#", style="dim", width=4, justify="right")
        table.add_column("Domain", style="cyan")
        table.add_column("Items", justify="right", style="green")

        for i, domain in enumerate(domains, 1):
            table.add_row(str(i), domain.name, f"{domain.count:,}")

        console.print(table)

    except ThinkAIError as e:
        console.print(f"[bold red]❌ Failed to load domains: {e.message}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def config(ctx):
    """Show current configuration"""
    config = ctx.obj["config"]

    config_text = (
        f"Server URL: [cyan]{config.base_url}[/cyan]\n"
        f"Timeout: [cyan]{config.timeout}s[/cyan]\n"
        f"Debug Mode: [cyan]{'enabled' if config.debug else 'disabled'}[/cyan]"
    )

    config_panel = Panel(
        config_text, title="⚙️ Think AI Configuration", border_style="blue"
    )
    console.print(config_panel)


@cli.command()
@click.pass_context
def ping(ctx):
    """Test connection to Think AI"""
    config = ctx.obj["config"]
    client = create_client(config)

    try:
        start_time = time.time()

        with console.status("[bold blue]Testing connection..."):
            is_online = client.ping()

        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        if is_online:
            console.print(
                f"[bold green]✅ Connected! Latency: {latency:.0f}ms[/bold green]"
            )
            console.print("[green]Think AI is online and responding[/green]")
        else:
            console.print("[bold red]❌ Connection failed[/bold red]")
            console.print("[red]Think AI is not responding[/red]")
            sys.exit(1)

    except Exception as e:
        console.print(f"[bold red]❌ Connection error: {e}[/bold red]")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]👋 Goodbye![/bold yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
