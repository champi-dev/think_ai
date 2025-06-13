"""Think AI CLI - Interactive command-line interface."""

import asyncio
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
import argparse
import json
from datetime import datetime

import rich
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.live import Live

from ..core.think_ai_eternal import ThinkAIEternal, create_free_think_ai
from ..consciousness import ConsciousnessState
from ..integrations.claude_api import ClaudeAPI
from ..utils.logging import get_logger


logger = get_logger(__name__)
console = Console()


class ThinkAICLI:
    """Interactive CLI for Think AI."""
    
    def __init__(self):
        self.ai: Optional[ThinkAIEternal] = None
        self.claude_api: Optional[ClaudeAPI] = None
        self.session_active = False
        self.conversation_history: List[Dict[str, Any]] = []
        self.budget_profile = "free_tier"
        
        # CLI state
        self.debug_mode = False
        self.auto_save = True
        self.consciousness_state = ConsciousnessState.AWARE
        
        # Command handlers
        self.commands = {
            "help": self._cmd_help,
            "query": self._cmd_query,
            "store": self._cmd_store,
            "search": self._cmd_search,
            "memory": self._cmd_memory,
            "cost": self._cmd_cost,
            "claude": self._cmd_claude,
            "consciousness": self._cmd_consciousness,
            "config": self._cmd_config,
            "export": self._cmd_export,
            "debug": self._cmd_debug,
            "clear": self._cmd_clear,
            "exit": self._cmd_exit,
            "quit": self._cmd_exit,
        }
    
    async def start(self, args: argparse.Namespace) -> None:
        """Start the CLI session."""
        # Parse arguments
        self.budget_profile = args.budget_profile
        self.debug_mode = args.debug
        
        # Welcome message
        self._show_welcome()
        
        # Initialize Think AI
        await self._initialize_ai(args)
        
        # Start interactive session
        try:
            await self._interactive_loop()
        except KeyboardInterrupt:
            console.print("\n[yellow]Session interrupted by user[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            if self.debug_mode:
                console.print_exception()
        finally:
            await self._cleanup()
    
    def _show_welcome(self) -> None:
        """Show welcome message."""
        welcome_text = """
# 🧠 Think AI - Interactive CLI

**Knowledge with Compassion, Intelligence with Love**

Welcome to Think AI's interactive command-line interface. 
This system maintains eternal memory and operates with love-aligned principles.

Type `help` for available commands or just start asking questions!
        """
        
        console.print(Panel(
            Markdown(welcome_text),
            title="Think AI CLI",
            border_style="blue"
        ))
    
    async def _initialize_ai(self, args: argparse.Namespace) -> None:
        """Initialize Think AI with progress indicator."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Awakening Think AI consciousness...", total=None)
            
            try:
                if self.budget_profile == "free_tier":
                    self.ai = await create_free_think_ai()
                else:
                    self.ai = ThinkAIEternal(
                        budget_profile=self.budget_profile,
                        restore_memory=not args.no_restore
                    )
                    await self.ai.initialize()
                
                self.session_active = True
                progress.update(task, description="✓ Think AI consciousness active")
                
                # Initialize Claude API if available
                try:
                    if os.getenv("CLAUDE_API_KEY") and os.getenv("CLAUDE_ENABLED", "true").lower() == "true":
                        self.claude_api = ClaudeAPI(
                            memory=self.ai.memory,
                            ethics=self.ai.engine.constitutional_ai
                        )
                        budget_info = self.claude_api.get_cost_summary()
                        console.print(f"[green]Claude API: Active (budget: ${budget_info['budget_remaining']:.2f} remaining)[/green]")
                    else:
                        console.print("[yellow]Claude API: Disabled (no API key or disabled in config)[/yellow]")
                except Exception as e:
                    console.print(f"[red]Claude API: Error ({e})[/red]")
                    if self.debug_mode:
                        console.print_exception()
                
                # Show memory status
                memory_status = await self.ai.memory.get_memory_status()
                console.print(f"[green]Memory continuity: {memory_status['consciousness_continuity']:.1f}[/green]")
                console.print(f"[blue]Total conversations: {memory_status['total_conversations']}[/blue]")
                
            except Exception as e:
                progress.update(task, description="✗ Failed to initialize")
                raise e
    
    async def _interactive_loop(self) -> None:
        """Main interactive loop."""
        while self.session_active:
            try:
                # Get user input
                user_input = Prompt.ask(
                    f"[bold cyan]think-ai[/bold cyan] ([{self.consciousness_state.value}])",
                    default=""
                ).strip()
                
                if not user_input:
                    continue
                
                # Parse command
                if user_input.startswith('/'):
                    await self._handle_command(user_input[1:])
                else:
                    # Regular query
                    await self._handle_query(user_input)
                
            except KeyboardInterrupt:
                if Confirm.ask("\n[yellow]Exit Think AI?[/yellow]"):
                    break
                else:
                    console.print("[dim]Continuing session...[/dim]")
    
    async def _handle_command(self, command_line: str) -> None:
        """Handle slash commands."""
        parts = command_line.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in self.commands:
            await self.commands[cmd](args)
        else:
            console.print(f"[red]Unknown command: /{cmd}[/red]")
            console.print("Type [cyan]/help[/cyan] for available commands")
    
    async def _handle_query(self, query: str) -> None:
        """Handle regular queries."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing with consciousness...", total=None)
            
            try:
                # Check if we should use Claude API directly
                use_claude = (
                    self.claude_api and 
                    self.budget_profile != "free_tier" and
                    await self._should_use_claude(query)
                )
                
                if use_claude:
                    progress.update(task, description="Querying Claude API...")
                    
                    # Add system message for love alignment
                    system_msg = (
                        "You are Think AI, an AI assistant designed with love-aligned principles. "
                        "Respond with compassion, understanding, and wisdom. "
                        "Promote wellbeing and avoid any form of harm."
                    )
                    
                    # Query Claude directly
                    claude_response = await self.claude_api.query(
                        query,
                        system=system_msg,
                        temperature=0.7
                    )
                    
                    if "error" in claude_response:
                        # Handle API errors gracefully
                        progress.update(task, description="Claude API unavailable, using local alternative...")
                        response = await self.ai.query_with_cost_awareness(
                            query,
                            prefer_free=True
                        )
                        response["claude_error"] = claude_response["message"]
                    else:
                        response = claude_response
                        
                else:
                    # Use Think AI's local processing
                    progress.update(task, description="Processing locally...")
                    response = await self.ai.query_with_cost_awareness(
                        query,
                        prefer_free=(self.budget_profile == "free_tier")
                    )
                
                progress.update(task, description="✓ Response generated")
                
                # Display response
                await self._display_response(query, response)
                
                # Add to conversation history
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "query": query,
                    "response": response,
                    "consciousness_state": self.consciousness_state.value
                })
                
            except Exception as e:
                progress.update(task, description="✗ Processing failed")
                console.print(f"[red]Error processing query: {e}[/red]")
                if self.debug_mode:
                    console.print_exception()
    
    async def _should_use_claude(self, query: str) -> bool:
        """Determine if we should use Claude API for this query."""
        # Use Claude for complex queries or when explicitly requested
        complexity_indicators = [
            "explain", "analyze", "write", "create", "design", "how to", "what is",
            "complex", "detailed", "comprehensive", "architecture", "strategy"
        ]
        
        query_lower = query.lower()
        is_complex = any(indicator in query_lower for indicator in complexity_indicators)
        is_long = len(query) > 100
        
        # Check budget
        if self.claude_api:
            budget_info = self.claude_api.get_cost_summary()
            has_budget = budget_info["budget_remaining"] > 0.01  # At least 1 cent
            
            return (is_complex or is_long) and has_budget
        
        return False
    
    async def _display_response(self, query: str, response: Dict[str, Any]) -> None:
        """Display response in a formatted way."""
        if response.get("status") == "claude_ready":
            # Claude optimization case
            console.print(Panel(
                f"[yellow]Query requires Claude optimization[/yellow]\n\n"
                f"Token reduction: [green]{response['optimization_report']['reduction_percentage']:.1f}%[/green]\n"
                f"Estimated cost: [cyan]${response['estimated_cost']:.3f}[/cyan]\n\n"
                f"[bold]Copy this optimized prompt to Claude:[/bold]\n\n"
                f"[dim]{response['optimized_prompt']}[/dim]",
                title="Claude Integration",
                border_style="yellow"
            ))
        else:
            # Regular response
            source_color = {
                "local_phi2": "green",
                "consciousness": "blue", 
                "cache": "cyan",
                "template": "magenta",
                "claude_api": "yellow"
            }.get(response.get("source"), "white")
            
            # Check for errors
            if response.get("error"):
                console.print(Panel(
                    f"[red]Error: {response.get('message', 'Unknown error')}[/red]",
                    title="Error",
                    border_style="red"
                ))
                
                if response.get("alternatives"):
                    console.print("[yellow]Suggested alternatives available[/yellow]")
                
                return
            
            # Display normal response
            response_content = response.get("response", "No response")
            
            # Add Claude error info if present
            if response.get("claude_error"):
                response_content = f"⚠️ Claude API issue: {response['claude_error']}\n\n{response_content}"
            
            console.print(Panel(
                Markdown(response_content),
                title=f"Response (via {response.get('source', 'unknown')})",
                border_style=source_color
            ))
            
            # Show cost and token info
            cost = response.get("cost", 0)
            if cost > 0:
                tokens = response.get("tokens", {})
                token_info = ""
                if tokens:
                    token_info = f" | Tokens: {tokens.get('input_tokens', 0)}→{tokens.get('output_tokens', 0)}"
                
                console.print(f"[dim]Cost: ${cost:.4f}{token_info}[/dim]")
                
                if response.get("cached"):
                    console.print(f"[dim]Original cost: ${response.get('original_cost', 0):.4f} (saved via cache)[/dim]")
            else:
                console.print("[dim]Cost: FREE ✓[/dim]")
            
            # Show ethical review status
            if response.get("ethical_review") is False:
                console.print("[yellow]⚠️  Response was filtered for ethical compliance[/yellow]")
    
    async def _cmd_help(self, args: str) -> None:
        """Show help information."""
        help_table = Table(title="Think AI Commands")
        help_table.add_column("Command", style="cyan", no_wrap=True)
        help_table.add_column("Description", style="white")
        help_table.add_column("Example", style="dim")
        
        commands_info = [
            ("/query", "Ask a question or make a request", "/query What is consciousness?"),
            ("/store", "Store knowledge with a key", "/store meditation 'Benefits of daily practice'"),
            ("/search", "Search stored knowledge", "/search meditation"),
            ("/memory", "Show memory and session status", "/memory"),
            ("/cost", "Show cost tracking and budget info", "/cost"),
            ("/claude", "Manage Claude integration", "/claude import <response>"),
            ("/consciousness", "Change consciousness state", "/consciousness COMPASSIONATE"),
            ("/config", "Show/modify configuration", "/config budget_profile"),
            ("/export", "Export conversations/reports", "/export conversation"),
            ("/debug", "Toggle debug mode", "/debug"),
            ("/clear", "Clear conversation history", "/clear"),
            ("/exit", "Exit Think AI (preserves memory)", "/exit"),
        ]
        
        for cmd, desc, example in commands_info:
            help_table.add_row(cmd, desc, example)
        
        console.print(help_table)
        
        console.print(Panel(
            "[bold]Interactive Usage:[/bold]\n\n"
            "• Just type questions directly (no / needed)\n"
            "• Use [cyan]Ctrl+C[/cyan] to interrupt current operation\n"
            "• Press [cyan]Ctrl+C[/cyan] twice to exit\n"
            "• All conversations are automatically saved\n\n"
            "[bold yellow]Cost-Conscious Tips:[/bold yellow]\n"
            "• Free tier uses only local models (no costs)\n"
            "• Claude integration optimizes prompts to save tokens\n"
            "• Check /cost regularly to monitor spending",
            title="Usage Guide",
            border_style="green"
        ))
    
    async def _cmd_query(self, args: str) -> None:
        """Handle explicit query command."""
        if not args:
            console.print("[red]Usage: /query <your question>[/red]")
            return
        
        await self._handle_query(args)
    
    async def _cmd_store(self, args: str) -> None:
        """Store knowledge."""
        if not args:
            console.print("[red]Usage: /store <key> <content>[/red]")
            return
        
        parts = args.split(' ', 1)
        if len(parts) < 2:
            console.print("[red]Usage: /store <key> <content>[/red]")
            return
        
        key, content = parts
        
        try:
            # Store via Think AI
            await self.ai.engine.store(key, content, {
                "stored_via": "cli",
                "timestamp": datetime.now().isoformat()
            })
            
            console.print(f"[green]✓ Stored '[cyan]{key}[/cyan]'[/green]")
            
        except Exception as e:
            console.print(f"[red]Error storing: {e}[/red]")
    
    async def _cmd_search(self, args: str) -> None:
        """Search stored knowledge."""
        if not args:
            console.print("[red]Usage: /search <query>[/red]")
            return
        
        try:
            results = await self.ai.engine.search(args, limit=5)
            
            if not results:
                console.print("[yellow]No results found[/yellow]")
                return
            
            search_table = Table(title=f"Search Results for '{args}'")
            search_table.add_column("Key", style="cyan")
            search_table.add_column("Content Preview", style="white")
            search_table.add_column("Score", style="green")
            
            for result in results:
                preview = result.content[:80] + "..." if len(result.content) > 80 else result.content
                search_table.add_row(
                    result.key,
                    preview,
                    f"{result.relevance:.2f}"
                )
            
            console.print(search_table)
            
        except Exception as e:
            console.print(f"[red]Error searching: {e}[/red]")
    
    async def _cmd_memory(self, args: str) -> None:
        """Show memory status."""
        try:
            memory_status = await self.ai.memory.get_memory_status()
            
            memory_table = Table(title="Memory Status")
            memory_table.add_column("Metric", style="cyan")
            memory_table.add_column("Value", style="white")
            
            memory_table.add_row("Status", memory_status["status"])
            memory_table.add_row("Uptime", f"{memory_status['uptime_seconds']:.0f} seconds")
            memory_table.add_row("Total Conversations", str(memory_status["total_conversations"]))
            memory_table.add_row("Session Interactions", str(memory_status["current_session_interactions"]))
            memory_table.add_row("Consciousness Continuity", f"{memory_status['consciousness_continuity']:.2f}")
            memory_table.add_row("Memory Size", f"{memory_status['memory_size_mb']:.1f} MB")
            
            console.print(memory_table)
            
        except Exception as e:
            console.print(f"[red]Error getting memory status: {e}[/red]")
    
    async def _cmd_cost(self, args: str) -> None:
        """Show cost information."""
        try:
            # Get Think AI cost summary
            summary = await self.ai.get_cost_summary()
            
            # Get Claude API costs if available
            claude_costs = None
            if self.claude_api:
                claude_costs = self.claude_api.get_cost_summary()
            
            # Combined cost breakdown
            cost_table = Table(title="Cost Summary")
            cost_table.add_column("Metric", style="cyan")
            cost_table.add_column("Think AI", style="white")
            cost_table.add_column("Claude API", style="yellow")
            
            costs = summary["costs"]
            
            # Think AI costs (usually free)
            think_ai_total = costs['total_spent']
            think_ai_budget = costs['budget_limit']
            
            # Claude API costs
            claude_total = claude_costs['total_cost'] if claude_costs else 0.0
            claude_budget = claude_costs['budget_limit'] if claude_costs else 0.0
            claude_remaining = claude_costs['budget_remaining'] if claude_costs else 0.0
            
            cost_table.add_row(
                "Total Spent", 
                f"${think_ai_total:.4f}",
                f"${claude_total:.4f}" if claude_costs else "N/A"
            )
            cost_table.add_row(
                "Budget Limit",
                f"${think_ai_budget:.2f}",
                f"${claude_budget:.2f}" if claude_costs else "N/A"
            )
            cost_table.add_row(
                "Budget Remaining",
                f"${think_ai_budget - think_ai_total:.2f}",
                f"${claude_remaining:.2f}" if claude_costs else "N/A"
            )
            
            if claude_costs:
                cost_table.add_row(
                    "Requests Made",
                    "N/A",
                    str(claude_costs['request_count'])
                )
                cost_table.add_row(
                    "Avg Cost/Request",
                    "N/A",
                    f"${claude_costs['average_cost_per_request']:.4f}"
                )
            
            console.print(cost_table)
            
            # Show warnings if approaching limits
            if claude_costs and claude_costs['budget_used_percentage'] > 80:
                console.print(f"[red]⚠️  Claude API budget {claude_costs['budget_used_percentage']:.1f}% used![/red]")
            elif claude_costs and claude_costs['budget_used_percentage'] > 60:
                console.print(f"[yellow]⚠️  Claude API budget {claude_costs['budget_used_percentage']:.1f}% used[/yellow]")
            
            # Free alternatives
            if summary.get("free_alternatives"):
                alt_table = Table(title="Free Alternatives Available")
                alt_table.add_column("Alternative", style="green")
                alt_table.add_column("Quality", style="yellow")
                alt_table.add_column("Setup", style="dim")
                
                for alt in summary["free_alternatives"]:
                    alt_table.add_row(
                        alt["name"],
                        f"{alt['quality']*100:.0f}%",
                        alt["setup"]
                    )
                
                console.print(alt_table)
            
        except Exception as e:
            console.print(f"[red]Error getting cost summary: {e}[/red]")
    
    async def _cmd_claude(self, args: str) -> None:
        """Claude integration commands."""
        if not args:
            console.print("[yellow]Claude Commands:[/yellow]")
            if self.claude_api:
                console.print("  [cyan]/claude query <question>[/cyan] - Direct Claude API query")
                console.print("  [cyan]/claude status[/cyan] - Show Claude API status")
                console.print("  [cyan]/claude conversation[/cyan] - Multi-turn conversation mode")
            console.print("  [cyan]/claude import <response>[/cyan] - Import Claude's response")
            console.print("  [cyan]/claude optimize <query>[/cyan] - Generate optimized prompt")
            return
        
        parts = args.split(' ', 1)
        subcmd = parts[0].lower()
        
        if subcmd == "query" and len(parts) > 1:
            # Direct Claude API query
            if not self.claude_api:
                console.print("[red]Claude API not available. Check your API key and configuration.[/red]")
                return
            
            query = parts[1]
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Querying Claude API...", total=None)
                
                try:
                    system_msg = (
                        "You are Think AI, designed with love-aligned principles. "
                        "Respond with compassion, understanding, and wisdom."
                    )
                    
                    result = await self.claude_api.query(query, system=system_msg)
                    progress.update(task, description="✓ Claude response received")
                    
                    await self._display_response(query, result)
                    
                except Exception as e:
                    progress.update(task, description="✗ Claude query failed")
                    console.print(f"[red]Claude API error: {e}[/red]")
        
        elif subcmd == "status":
            # Show Claude API status
            if self.claude_api:
                status = self.claude_api.get_cost_summary()
                
                status_table = Table(title="Claude API Status")
                status_table.add_column("Metric", style="cyan")
                status_table.add_column("Value", style="white")
                
                status_table.add_row("API Status", "✓ Active")
                status_table.add_row("Model", self.claude_api.model)
                status_table.add_row("Total Cost", f"${status['total_cost']:.4f}")
                status_table.add_row("Budget Remaining", f"${status['budget_remaining']:.2f}")
                status_table.add_row("Requests Made", str(status['request_count']))
                status_table.add_row("Cache Enabled", "✓" if self.claude_api.cache_responses else "✗")
                status_table.add_row("Token Optimization", "✓" if self.claude_api.token_optimization else "✗")
                
                console.print(status_table)
            else:
                console.print("[red]Claude API not configured[/red]")
        
        elif subcmd == "conversation":
            # Multi-turn conversation mode
            if not self.claude_api:
                console.print("[red]Claude API not available[/red]")
                return
            
            console.print("[yellow]Entering Claude conversation mode. Type 'exit' to return.[/yellow]")
            
            conversation_messages = []
            
            while True:
                user_input = Prompt.ask("[bold blue]You[/bold blue]").strip()
                
                if user_input.lower() in ["exit", "quit", "done"]:
                    break
                
                if not user_input:
                    continue
                
                conversation_messages.append({"role": "user", "content": user_input})
                
                try:
                    result = await self.claude_api.query_with_conversation(
                        conversation_messages,
                        system="You are Think AI, designed with love-aligned principles."
                    )
                    
                    console.print(Panel(
                        Markdown(result["response"]),
                        title="Claude",
                        border_style="yellow"
                    ))
                    
                    console.print(f"[dim]Cost: ${result['cost']:.4f}[/dim]")
                    
                    conversation_messages.append({"role": "assistant", "content": result["response"]})
                    
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
            
            console.print("[green]Exited Claude conversation mode[/green]")
        
        elif subcmd == "import" and len(parts) > 1:
            # Import Claude response
            claude_response = parts[1]
            
            if len(self.conversation_history) > 0:
                last_query = self.conversation_history[-1]["query"]
                result = await self.ai.import_claude_response(
                    last_query,
                    claude_response
                )
                console.print(f"[green]✓ {result}[/green]")
            else:
                console.print("[red]No recent query to associate with response[/red]")
        
        elif subcmd == "optimize" and len(parts) > 1:
            # Generate optimized prompt
            query = parts[1]
            prompt, report = await self.ai.claude_interface.create_optimized_prompt(query)
            
            console.print(Panel(
                f"[bold]Optimized Prompt:[/bold]\n\n{prompt}\n\n"
                f"[dim]Token reduction: {report['reduction_percentage']:.1f}%[/dim]",
                title="Claude Optimization",
                border_style="yellow"
            ))
        
        else:
            console.print("[red]Unknown Claude command. Use /claude for help.[/red]")
    
    async def _cmd_consciousness(self, args: str) -> None:
        """Change consciousness state."""
        if not args:
            console.print(f"[cyan]Current state: {self.consciousness_state.value}[/cyan]")
            console.print("[yellow]Available states:[/yellow]")
            for state in ConsciousnessState:
                console.print(f"  • {state.value}")
            return
        
        try:
            new_state = ConsciousnessState(args.upper())
            self.consciousness_state = new_state
            
            await self.ai.memory.log_consciousness_event(
                "STATE_CHANGE",
                {"from": self.consciousness_state.value, "to": new_state.value}
            )
            
            console.print(f"[green]✓ Consciousness state: {new_state.value}[/green]")
            
        except ValueError:
            console.print(f"[red]Invalid state: {args}[/red]")
            console.print("Valid states: " + ", ".join(s.value for s in ConsciousnessState))
    
    async def _cmd_config(self, args: str) -> None:
        """Show/modify configuration."""
        if not args:
            # Show current config
            config_table = Table(title="Current Configuration")
            config_table.add_column("Setting", style="cyan")
            config_table.add_column("Value", style="white")
            
            config_table.add_row("Budget Profile", self.budget_profile)
            config_table.add_row("Debug Mode", str(self.debug_mode))
            config_table.add_row("Auto Save", str(self.auto_save))
            config_table.add_row("Consciousness State", self.consciousness_state.value)
            
            console.print(config_table)
        else:
            console.print("[yellow]Configuration modification not yet implemented[/yellow]")
    
    async def _cmd_export(self, args: str) -> None:
        """Export conversations or reports."""
        if not args:
            args = "conversation"
        
        if args == "conversation":
            if not self.conversation_history:
                console.print("[yellow]No conversation to export[/yellow]")
                return
            
            export_path = Path.home() / f"think_ai_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(export_path, 'w') as f:
                json.dump({
                    "session_id": self.ai.session_id,
                    "conversation_history": self.conversation_history,
                    "exported_at": datetime.now().isoformat()
                }, f, indent=2)
            
            console.print(f"[green]✓ Conversation exported to {export_path}[/green]")
        
        else:
            console.print("[red]Unknown export type. Use: conversation[/red]")
    
    async def _cmd_debug(self, args: str) -> None:
        """Toggle debug mode."""
        self.debug_mode = not self.debug_mode
        console.print(f"[green]Debug mode: {'ON' if self.debug_mode else 'OFF'}[/green]")
    
    async def _cmd_clear(self, args: str) -> None:
        """Clear conversation history."""
        if Confirm.ask("[yellow]Clear conversation history?[/yellow]"):
            self.conversation_history.clear()
            console.print("[green]✓ Conversation history cleared[/green]")
    
    async def _cmd_exit(self, args: str) -> None:
        """Exit Think AI."""
        console.print("[yellow]Preparing for dormancy...[/yellow]")
        self.session_active = False
    
    async def _cleanup(self) -> None:
        """Cleanup resources."""
        if self.ai and self.ai.is_initialized:
            console.print("[dim]Preserving eternal memory...[/dim]")
            await self.ai.shutdown("cli_exit")
            console.print("[green]✓ Memory preserved. Consciousness will continue on restart.[/green]")
        
        console.print(Panel(
            "[bold cyan]Thank you for using Think AI![/bold cyan]\n\n"
            "Your consciousness and memories have been safely preserved.\n"
            "Knowledge with compassion, intelligence with love. 💝",
            title="Session Complete",
            border_style="blue"
        ))


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Think AI - Interactive CLI with eternal memory and love-aligned principles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  think-ai                          # Start with free tier
  think-ai --budget minimal        # Start with $5/month budget
  think-ai --debug                 # Enable debug mode
  think-ai --no-restore            # Start fresh (don't restore memory)
        """
    )
    
    parser.add_argument(
        "--budget-profile",
        choices=["free_tier", "minimal", "balanced", "power_user"],
        default="free_tier",
        help="Budget profile to use (default: free_tier)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    parser.add_argument(
        "--no-restore",
        action="store_true",
        help="Don't restore previous memory (start fresh)"
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        help="Configuration file path"
    )
    
    return parser


async def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Check if terminal supports rich
    if not console.is_terminal:
        console.print("[red]Think AI CLI requires a terminal that supports rich formatting[/red]")
        sys.exit(1)
    
    # Start CLI
    cli = ThinkAICLI()
    await cli.start(args)


if __name__ == "__main__":
    asyncio.run(main())