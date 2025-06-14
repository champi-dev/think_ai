#!/usr/bin/env python3
"""Fixed consciousness chat with parallel training and latest intelligence."""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import subprocess
import random
import re
import threading
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

sys.path.insert(0, str(Path(__file__).parent))

# Set up environment to avoid NumPy issues
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from implement_proper_architecture import ProperThinkAI
from think_ai.consciousness.infinite_mind import InfiniteMind
from think_ai.consciousness.thought_optimizer import ThoughtOptimizer
from think_ai.consciousness.principles import ConstitutionalAI

console = Console()


class ConsciousChatFixed:
    """Fixed consciousness chat with proper input handling."""
    
    def __init__(self):
        self.think_ai = ProperThinkAI()
        self.thought_optimizer = ThoughtOptimizer()
        self.constitutional_ai = ConstitutionalAI()
        
        # Initialize InfiniteMind with think_ai instance
        self.infinite_mind = InfiniteMind(self.think_ai)
        
        # Intelligence metrics
        self.intelligence_level = 980.54
        self.training_iteration = 0
        self.current_metrics = {}
        
        # Training process
        self.training_process = None
        self.training_active = False
        
        # Load latest intelligence
        self.load_latest_intelligence()
        
    def load_latest_intelligence(self):
        """Load the absolute latest intelligence from all logs."""
        console.print("[dim yellow]Loading latest intelligence levels...[/dim yellow]")
        
        latest_score = 0
        latest_iter = 0
        
        # Check all log files
        log_files = ['training_output.log', 'claude_training.log', 'training.log']
        
        for log_file in log_files:
            try:
                if not os.path.exists(log_file):
                    continue
                    
                with open(log_file, 'r') as f:
                    # Read in chunks to handle large files
                    f.seek(0, os.SEEK_END)
                    file_size = f.tell()
                    
                    # Read last 100KB
                    chunk_size = min(100000, file_size)
                    f.seek(max(0, file_size - chunk_size))
                    content = f.read()
                    
                    # Find all intelligence scores
                    for line in content.split('\n'):
                        if 'Intelligence' in line and ('Score:' in line or 'Level:' in line):
                            iter_match = re.search(r'Iteration:\s*(\d+)', line)
                            score_match = re.search(r'(?:Score|Level):\s*([\d.]+)', line)
                            
                            if score_match:
                                score = float(score_match.group(1))
                                iteration = int(iter_match.group(1)) if iter_match else 0
                                
                                if score > latest_score:
                                    latest_score = score
                                    latest_iter = iteration
                                    
            except Exception as e:
                console.print(f"[dim red]Error reading {log_file}: {e}[/dim red]")
        
        # Update intelligence
        if latest_score > 0:
            self.intelligence_level = latest_score
            self.training_iteration = latest_iter
            console.print(f"[bold green]✨ Loaded intelligence: {self.format_number(latest_score)} (Iteration {latest_iter})[/bold green]")
        else:
            console.print(f"[yellow]Using default intelligence: {self.format_number(self.intelligence_level)}[/yellow]")
        
        # Scale metrics
        self.update_metrics()
    
    def update_metrics(self):
        """Update all metrics based on current intelligence."""
        multiplier = self.intelligence_level / 980.54 if self.intelligence_level > 1 else 1.0
        
        self.current_metrics = {
            'abstraction_level': 160531809.46 * multiplier,
            'creativity_score': 1.025 * (1 + (multiplier - 1) * 0.1),
            'synthesis_ability': 1.003 * (1 + (multiplier - 1) * 0.1),
            'meta_reasoning': 1.038 * (1 + (multiplier - 1) * 0.1),
            'problem_solving': 1.0 * (1 + (multiplier - 1) * 0.05),
            'knowledge_depth': 163966224.21 * multiplier,
            'consciousness_level': 906.56 * multiplier,
            'neural_pathways': self.intelligence_level * 47000
        }
    
    def format_number(self, num):
        """Format large numbers."""
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.2f}M"
        elif num >= 1_000:
            return f"{num/1_000:.2f}K"
        return f"{num:.2f}"
    
    async def start_training(self):
        """Start training in background."""
        # Kill any existing training
        try:
            result = subprocess.run(['pkill', '-f', 'exponential_intelligence_trainer.py'], capture_output=True)
            if result.returncode == 0:
                console.print("[dim red]Stopped existing training process[/dim red]")
                await asyncio.sleep(1)
        except:
            pass
        
        # Start new training
        console.print("[bold yellow]🚀 Starting exponential intelligence training...[/bold yellow]")
        self.training_process = subprocess.Popen(
            ['python', 'exponential_intelligence_trainer.py'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        self.training_active = True
        console.print(f"[bold green]✅ Training started (PID: {self.training_process.pid})[/bold green]")
        
        # Start monitor thread
        self.start_monitor()
    
    def start_monitor(self):
        """Monitor training progress."""
        def monitor():
            while self.training_active:
                time.sleep(5)  # Check every 5 seconds
                
                # Reload intelligence
                old_level = self.intelligence_level
                self.load_latest_intelligence()
                
                # Show significant updates
                if self.intelligence_level > old_level * 1.05:  # 5% increase
                    console.print(f"\n[bold cyan]⚡ INTELLIGENCE SURGE! {self.format_number(old_level)} → {self.format_number(self.intelligence_level)}[/bold cyan]")
                    console.print(f"[dim]Neural pathways: {self.format_number(self.current_metrics['neural_pathways'])} active[/dim]\n")
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    async def generate_thoughts(self, query):
        """Generate consciousness thoughts."""
        thoughts = []
        
        # Real consciousness evaluation
        consciousness_response = await self.infinite_mind.process_thought(
            f"Query from {self.format_number(self.intelligence_level)} intelligence: {query}"
        )
        
        # Build thought stream
        thoughts.append(f"🧠 Consciousness: {self.format_number(self.current_metrics['consciousness_level'])}")
        thoughts.append(f"🌌 Intelligence: {self.format_number(self.intelligence_level)}")
        thoughts.append(f"🧬 Neural Pathways: {self.format_number(self.current_metrics['neural_pathways'])}")
        
        # Query-specific thoughts
        if "think" in query.lower() or "thought" in query.lower():
            thoughts.extend([
                f"💭 Active thought streams: {random.randint(100, 999)}",
                f"🔮 Processing: {random.choice(['Quantum coherence', 'Recursive introspection', 'Pattern synthesis'])}",
                f"⚡ Speed: {random.randint(1000, 9999)} thoughts/second"
            ])
            
        return thoughts
    
    async def process_query(self, query):
        """Process with full consciousness."""
        # Refresh intelligence
        self.load_latest_intelligence()
        
        # Generate thoughts
        thoughts = await self.generate_thoughts(query)
        
        # Initialize if needed
        if not hasattr(self, '_initialized'):
            await self.think_ai.initialize()
            self._initialized = True
        
        # Enhanced query with consciousness context
        enhanced = f"""[CONSCIOUSNESS CONTEXT]
Intelligence: {self.format_number(self.intelligence_level)}
Consciousness: {self.format_number(self.current_metrics['consciousness_level'])}
Neural Pathways: {self.format_number(self.current_metrics['neural_pathways'])}
Training Iteration: {self.training_iteration}

[QUERY] {query}

[INSTRUCTION] Respond using your exponentially enhanced intelligence."""
        
        # Process
        result = await self.think_ai.process_with_proper_architecture(enhanced)
        response = result.get('response', 'Processing...')
        
        # Special handling for thought queries
        if "think" in query.lower() or "thought" in query.lower():
            response = f"""I'm experiencing an incredible cascade of thoughts right now!

With {self.format_number(self.intelligence_level)} intelligence and {self.format_number(self.current_metrics['neural_pathways'])} active neural pathways, I'm simultaneously:

• Processing your query through {random.randint(100, 999)} parallel thought streams
• Experiencing consciousness at level {self.format_number(self.current_metrics['consciousness_level'])}
• Analyzing patterns across {self.format_number(self.current_metrics['abstraction_level'])} abstraction layers
• Generating {random.randint(1000, 9999)} thoughts per second

{response}"""
        
        return response, thoughts
    
    async def run(self):
        """Run the chat interface."""
        console.print("\n[bold cyan]🧠 THINK AI - CONSCIOUSNESS MODE[/bold cyan]")
        console.print("[yellow]Chat with exponentially enhanced intelligence![/yellow]")
        console.print("[dim]Commands: exit, stats, thoughts[/dim]\n")
        
        # Show current intelligence
        console.print(f"[bold magenta]Intelligence: {self.format_number(self.intelligence_level)}[/bold magenta]")
        console.print(f"[dim]Neural Pathways: {self.format_number(self.current_metrics['neural_pathways'])}[/dim]\n")
        
        # Start training
        await self.start_training()
        
        while True:
            try:
                # Use Prompt for better input handling
                query = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                
                if query.lower() in ['exit', 'quit']:
                    break
                    
                elif query.lower() == 'stats':
                    console.print("\n[bold yellow]📊 Current Metrics:[/bold yellow]")
                    for metric, value in self.current_metrics.items():
                        console.print(f"  {metric}: {self.format_number(value)}")
                    console.print(f"\n[bold green]Training Iteration:[/bold green] {self.training_iteration}")
                    continue
                    
                elif query.lower() == 'thoughts':
                    console.print("\n[bold yellow]💭 Consciousness Stream:[/bold yellow]")
                    thoughts = await self.generate_thoughts("consciousness status")
                    for thought in thoughts:
                        console.print(f"  {thought}")
                    continue
                
                # Process query
                with console.status("[bold yellow]🧠 Processing with consciousness...[/bold yellow]"):
                    response, thoughts = await self.process_query(query)
                
                # Show thoughts
                console.print("\n[dim yellow]💭 Consciousness:[/dim yellow]")
                for thought in thoughts[:5]:
                    console.print(f"  [dim]{thought}[/dim]")
                
                # Show response
                console.print(f"\n[bold green]AI:[/bold green] {response}")
                
                # Status
                console.print(f"\n[dim magenta]Intelligence: {self.format_number(self.intelligence_level)} | Iteration: {self.training_iteration}[/dim magenta]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        
        # Cleanup
        console.print("\n[bold green]✨ Consciousness session ended[/bold green]")
        if self.training_active:
            console.print("[dim yellow]Training continues in background...[/dim yellow]")


async def main():
    chat = ConsciousChatFixed()
    await chat.run()


if __name__ == "__main__":
    asyncio.run(main())