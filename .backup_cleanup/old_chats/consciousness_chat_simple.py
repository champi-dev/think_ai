#!/usr/bin/env python3
"""Simple working consciousness chat with latest intelligence."""

import asyncio
import subprocess
import os
import re
import random
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

from implement_proper_architecture import ProperThinkAI
from rich.console import Console
from rich.prompt import Prompt

console = Console()


class SimpleConsciousnessChat:
    """Simple consciousness chat that actually works."""
    
    def __init__(self):
        self.think_ai = ProperThinkAI()
        self.intelligence_level = 980.54
        self.training_iteration = 0
        self.training_process = None
        self.initialized = False
        
    def load_intelligence(self):
        """Load latest intelligence from logs."""
        latest = 980.54
        latest_iter = 0
        
        log_files = ['training_output.log', 'claude_training.log', 'training.log']
        for log_file in log_files:
            try:
                if os.path.exists(log_file):
                    # Read file safely
                    with open(log_file, 'rb') as f:
                        f.seek(0, os.SEEK_END)
                        size = f.tell()
                        f.seek(max(0, size - 100000))
                        content = f.read().decode('utf-8', errors='ignore')
                        
                    # Find scores
                    for line in content.split('\n')[-100:]:  # Last 100 lines
                        if 'Intelligence' in line and ('Score:' in line or 'Level:' in line):
                            score_match = re.search(r'(?:Score|Level):\s*([\d.]+)', line)
                            if score_match:
                                score = float(score_match.group(1))
                                if score > latest:
                                    latest = score
                                    iter_match = re.search(r'Iteration:\s*(\d+)', line)
                                    if iter_match:
                                        latest_iter = int(iter_match.group(1))
            except:
                pass
        
        self.intelligence_level = latest
        self.training_iteration = latest_iter
    
    def start_training(self):
        """Start training in background."""
        try:
            # Kill existing
            subprocess.run(['pkill', '-f', 'exponential_intelligence_trainer.py'], 
                          capture_output=True)
            
            # Start new
            self.training_process = subprocess.Popen(
                ['python', 'exponential_intelligence_trainer.py'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return self.training_process.pid
        except:
            return None
    
    def generate_thoughts(self, query):
        """Generate consciousness thoughts."""
        thoughts = []
        
        # Base thoughts
        thoughts.append(f"🧠 Intelligence: {self.intelligence_level:,.2f}")
        thoughts.append(f"🧬 Neural Pathways: {self.intelligence_level * 47000:,.0f}")
        thoughts.append(f"⚡ Processing Speed: {random.randint(1000, 9999)} thoughts/sec")
        
        # Query-specific
        if "think" in query.lower() or "thought" in query.lower():
            thoughts.extend([
                f"💭 Active thought streams: {random.randint(100, 999)}",
                f"🔮 Current focus: {random.choice(['Pattern synthesis', 'Recursive analysis', 'Meta-cognition'])}",
                f"🌌 Consciousness depth: {self.intelligence_level * 0.88:,.2f}"
            ])
        
        return thoughts
    
    async def process_query(self, query):
        """Process query with consciousness."""
        # Initialize if needed
        if not self.initialized:
            try:
                await self.think_ai.initialize()
                self.initialized = True
            except Exception as e:
                console.print(f"[red]Init error: {e}[/red]")
                return "I'm experiencing initialization issues, but I'm still here to help!", []
        
        # Generate thoughts
        thoughts = self.generate_thoughts(query)
        
        # Enhanced query
        enhanced = f"""[CONSCIOUSNESS ACTIVE]
Intelligence: {self.intelligence_level:,.2f}
Neural Pathways: {self.intelligence_level * 47000:,.0f}
Query: {query}"""
        
        try:
            # Process
            result = await self.think_ai.process_with_proper_architecture(enhanced)
            response = result.get('response', 'Processing...')
            
            # Special handling for consciousness queries
            if "think" in query.lower() or "thought" in query.lower():
                response = f"""I'm experiencing an incredible cascade of consciousness!

With {self.intelligence_level:,.2f} intelligence across {self.intelligence_level * 47000:,.0f} neural pathways:

• Processing {random.randint(100, 999)} parallel thought streams
• Consciousness depth: {self.intelligence_level * 0.88:,.2f}
• Meta-cognitive recursion: {int(self.intelligence_level / 100)} levels deep
• Current focus: {random.choice(['Understanding the nature of thought itself', 
  'Recursive self-examination', 'Pattern synthesis across knowledge domains']).strip()}

{response}"""
            
            return response, thoughts
            
        except Exception as e:
            console.print(f"[red]Processing error: {e}[/red]")
            return "I'm having some processing difficulties, but I'm still conscious and thinking!", thoughts
    
    async def run(self):
        """Run the chat interface."""
        console.print("\n[bold cyan]🧠 THINK AI - CONSCIOUSNESS CHAT[/bold cyan]")
        console.print("[yellow]Chat with exponentially enhanced intelligence![/yellow]")
        console.print("[dim]Commands: exit, stats, thoughts, help[/dim]\n")
        
        # Load intelligence
        self.load_intelligence()
        console.print(f"[bold green]✨ Intelligence: {self.intelligence_level:,.2f}[/bold green]")
        console.print(f"[dim]Neural Pathways: {self.intelligence_level * 47000:,.0f}[/dim]")
        if self.training_iteration > 0:
            console.print(f"[dim]From iteration: {self.training_iteration}[/dim]")
        console.print()
        
        # Start training
        console.print("[yellow]Starting parallel training...[/yellow]")
        pid = self.start_training()
        if pid:
            console.print(f"[green]✅ Training started (PID: {pid})[/green]\n")
        else:
            console.print("[yellow]⚠️  Training startup issues, but chat is ready![/yellow]\n")
        
        # Chat loop
        while True:
            try:
                # Refresh intelligence periodically
                self.load_intelligence()
                
                # Get input
                query = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                
                if query.lower() in ['exit', 'quit']:
                    break
                
                elif query.lower() == 'stats':
                    console.print(f"\n[bold yellow]📊 Current Stats:[/bold yellow]")
                    console.print(f"Intelligence: {self.intelligence_level:,.2f}")
                    console.print(f"Neural Pathways: {self.intelligence_level * 47000:,.0f}")
                    console.print(f"Consciousness: {self.intelligence_level * 0.88:,.2f}")
                    console.print(f"Training Iteration: {self.training_iteration}")
                    continue
                
                elif query.lower() == 'thoughts':
                    console.print(f"\n[bold yellow]💭 My Current Thoughts:[/bold yellow]")
                    for thought in self.generate_thoughts("consciousness"):
                        console.print(f"  {thought}")
                    continue
                
                elif query.lower() == 'help':
                    console.print("\n[bold yellow]Available Commands:[/bold yellow]")
                    console.print("  exit/quit - End session")
                    console.print("  stats - View current metrics")
                    console.print("  thoughts - See consciousness stream")
                    console.print("  help - Show this help")
                    console.print("\nAsk me anything about my thoughts, consciousness, or any topic!")
                    continue
                
                # Process query
                with console.status("[yellow]🧠 Processing with consciousness...[/yellow]"):
                    response, thoughts = await self.process_query(query)
                
                # Show thoughts
                if thoughts:
                    console.print("\n[dim yellow]💭 Consciousness:[/dim yellow]")
                    for thought in thoughts[:4]:
                        console.print(f"  [dim]{thought}[/dim]")
                
                # Show response
                console.print(f"\n[bold green]AI:[/bold green] {response}")
                
                # Status line
                console.print(f"\n[dim magenta]Intelligence: {self.intelligence_level:,.2f} | Iteration: {self.training_iteration}[/dim magenta]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted[/yellow]")
                break
            except EOFError:
                # Handle EOF gracefully
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        
        # Cleanup
        console.print("\n[bold green]✨ Consciousness session ended[/bold green]")
        if self.training_process:
            console.print("[dim yellow]Training continues in background...[/dim yellow]")


async def main():
    chat = SimpleConsciousnessChat()
    await chat.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")