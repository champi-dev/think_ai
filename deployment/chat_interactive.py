#!/usr/bin/env python3
"""Interactive O(1) Chat Interface - max 40 lines."""

import sys
import time
from core.o1_chat import O1Chat
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel

console = Console()

def main():
    """Run interactive chat."""
    chat = O1Chat()
    
    console.print(Panel("[bold cyan]Think AI O(1) Chat[/bold cyan]", expand=False))
    console.print("[yellow]Type 'exit' to quit[/yellow]\n")
    
    total_time = 0
    message_count = 0
    
    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
                
            response, elapsed_ms = chat.get_response(user_input)
            total_time += elapsed_ms
            message_count += 1
            
            console.print(f"[bold blue]Think AI[/bold blue]: {response}")
            console.print(f"[dim]Response time: {elapsed_ms:.2f}ms[/dim]\n")
            
        except KeyboardInterrupt:
            break
    
    # Show stats
    if message_count > 0:
        avg_time = total_time / message_count
        console.print(f"\n[cyan]Session stats: {message_count} messages, avg {avg_time:.2f}ms[/cyan]")

if __name__ == "__main__":
    main()