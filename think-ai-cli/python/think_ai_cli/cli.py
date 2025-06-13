"""Think AI CLI - Command Line Interface."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from . import ThinkAI

console = Console()
ai = ThinkAI()


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """Think AI - AI-powered coding assistant with vector search."""


@cli.command()
@click.argument("query")
@click.option("-n", "--number", default=5, help="Number of results to return")
@click.option("-l", "--language", help="Filter by programming language")
def search(query, number, language) -> None:
    """Search for similar code patterns."""
    with console.status("[bold green]Searching..."):
        results = ai.search(query, k=number)

    if not results:
        console.print(
            "[yellow]No results found. Try adding some code first with 'think add'[/yellow]"
        )
        return

    console.print(f"\n[bold]Found {len(results)} similar code patterns:[/bold]\n")

    for i, (score, code, meta) in enumerate(results, 1):
        if language and meta["language"] != language:
            continue

        panel_title = f"{i}. {meta['description']} [dim]({meta['language']})[/dim] - {score*100:.1f}% match"

        syntax = Syntax(
            code[:500] + "..." if len(code) > 500 else code,
            meta["language"],
            theme="monokai",
            line_numbers=True,
        )

        console.print(Panel(syntax, title=panel_title, border_style="blue"))
        console.print()


@cli.command()
@click.option("-f", "--file", type=click.Path(exists=True), help="Code file to add")
@click.option("-c", "--code", help="Code snippet (alternative to file)")
@click.option("-l", "--language", required=True, help="Programming language")
@click.option("-d", "--description", required=True, help="Description of the code")
@click.option("-t", "--tags", multiple=True, help="Tags for categorization")
def add(file, code, language, description, tags) -> None:
    """Add code to the knowledge base."""
    if file:
        with open(file) as f:
            code_content = f.read()
    elif code:
        code_content = code
    else:
        console.print("[red]Error: Provide either --file or --code[/red]")
        return

    with console.status("[bold green]Adding to knowledge base..."):
        idx = ai.add_code(code_content, language, description, list(tags))

    console.print(f"[green]✓ Added successfully! (Index: {idx})[/green]")
    console.print(f"Description: {description}")
    console.print(f"Language: {language}")
    if tags:
        console.print(f"Tags: {', '.join(tags)}")


@cli.command()
@click.argument("prompt")
@click.option("-l", "--language", default="python", help="Target programming language")
@click.option("-o", "--output", type=click.Path(), help="Save to file")
def generate(prompt, language, output) -> None:
    """Generate code based on prompt."""
    with console.status(f"[bold green]Generating {language} code..."):
        generated_code = ai.generate_code(prompt, language)

    syntax = Syntax(generated_code, language, theme="monokai", line_numbers=True)
    console.print(
        Panel(syntax, title=f"Generated {language} code", border_style="green")
    )

    if output:
        with open(output, "w") as f:
            f.write(generated_code)
        console.print(f"[green]✓ Saved to {output}[/green]")


@cli.command()
@click.argument("file", type=click.Path(exists=True))
def analyze(file) -> None:
    """Analyze code file for patterns and suggestions."""
    with open(file) as f:
        code = f.read()

    # Language detection removed - not used in current analysis implementation

    with console.status("[bold green]Analyzing code..."):
        analysis = ai.analyze_code(code)

    # Display analysis results
    console.print(Panel(f"[bold]Code Analysis: {file}[/bold]", border_style="cyan"))

    # Basic metrics
    table = Table(title="Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Lines", str(analysis["lines"]))
    table.add_row("Characters", str(analysis["length"]))

    console.print(table)

    # Similar patterns
    if analysis["similar_patterns"]:
        console.print("\n[bold]Similar patterns found:[/bold]")
        for pattern in analysis["similar_patterns"]:
            console.print(
                f"  • {pattern['description']} ({pattern['similarity']} similar)"
            )

    # Suggestions
    if analysis["suggestions"]:
        console.print("\n[bold]Suggestions:[/bold]")
        for suggestion in analysis["suggestions"]:
            console.print(f"  💡 {suggestion}")


@cli.command()
def stats() -> None:
    """Show knowledge base statistics."""
    stats = ai.get_stats()

    console.print(
        Panel("[bold]Think AI Knowledge Base Statistics[/bold]", border_style="cyan")
    )

    table = Table()
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Code Snippets", str(stats["total_snippets"]))
    table.add_row("Total Characters", f"{stats['total_characters']:,}")
    table.add_row("Index Size", str(stats.get("index_size", 0)))

    console.print(table)

    if stats.get("languages"):
        console.print("\n[bold]Languages:[/bold]")
        for lang, count in stats["languages"].items():
            console.print(f"  • {lang}: {count} snippets")


@cli.command()
@click.confirmation_option(prompt="Are you sure you want to clear the knowledge base?")
def clear() -> None:
    """Clear the entire knowledge base."""
    ai.code_snippets = []
    ai.metadata = []
    ai.index = None
    ai._save_knowledge_base()
    console.print("[green]✓ Knowledge base cleared[/green]")


@cli.command()
def interactive() -> None:
    """Start interactive mode."""
    console.print(
        Panel(
            "[bold]Think AI Interactive Mode[/bold]\n"
            "Commands: search, add, generate, analyze, stats, help, exit",
            border_style="cyan",
        )
    )

    while True:
        try:
            command = console.input("\n[bold cyan]think>[/bold cyan] ")

            if command.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break
            if command.lower() == "help":
                console.print(
                    """
Commands:
  search <query>     - Search for code patterns
  generate <prompt>  - Generate code from prompt
  stats              - Show statistics
  exit               - Exit interactive mode
                """
                )
            elif command.startswith("search "):
                query = command[7:]
                results = ai.search(query, k=3)
                for i, (score, code, meta) in enumerate(results, 1):
                    console.print(
                        f"\n{i}. {meta['description']} ({score*100:.1f}% match)"
                    )
                    console.print(
                        Syntax(
                            code[:200] + "..." if len(code) > 200 else code,
                            meta["language"],
                            theme="monokai",
                        )
                    )
            elif command.startswith("generate "):
                prompt = command[9:]
                code = ai.generate_code(prompt)
                console.print(Syntax(code, "python", theme="monokai"))
            elif command == "stats":
                stats = ai.get_stats()
                console.print(f"Snippets: {stats['total_snippets']}")
            else:
                console.print(
                    "[red]Unknown command. Type 'help' for available commands.[/red]"
                )

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
