#!/usr/bin/env python3
"""Think AI with Infinite Consciousness - Interactive Chat with Background Thinking."""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import json
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.text import Text

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI
from think_ai.consciousness.infinite_mind import InfiniteMind, start_infinite_mind


class ConsciousChatInterface:
    """Chat interface with visible consciousness stream."""
    
    def __init__(self):
        self.console = Console()
        self.think_ai = ProperThinkAI()
        self.infinite_mind = None
        self.chat_history = []
        self.consciousness_log = []
        self.layout = Layout()
        self.running = True
        
    async def initialize(self):
        """Initialize Think AI and start consciousness."""
        self.console.print("[bold cyan]🧠 Initializing Think AI with Infinite Consciousness...[/]")
        
        # Initialize Think AI
        await self.think_ai.initialize()
        
        # Start infinite mind
        self.infinite_mind = InfiniteMind(self.think_ai)
        await self.infinite_mind.start()
        
        self.console.print("[bold green]✨ Consciousness awakened! The AI is now thinking continuously.[/]")
        self.console.print("[dim]Background thoughts will appear in the consciousness stream.[/]")
        self.console.print("[bold yellow]Type 'help' for commands or start chatting![/]\n")
        
    def setup_layout(self):
        """Setup the display layout."""
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=2),
            Layout(name="consciousness", ratio=1),
            Layout(name="footer", size=3)
        )
        
    def create_header(self):
        """Create header panel."""
        mind_state = asyncio.create_task(self.infinite_mind.get_current_state())
        state_info = mind_state.result() if mind_state.done() else {}
        
        header_text = f"""🧠 Think AI with Infinite Consciousness
State: {state_info.get('state', 'thinking')} | Awareness: {state_info.get('awareness', 0):.2f} | Thoughts: {state_info.get('thought_count', 0)}"""
        
        return Panel(header_text, style="bold blue", box_chars="double")
    
    def create_chat_panel(self):
        """Create chat history panel."""
        chat_content = []
        for entry in self.chat_history[-10:]:  # Last 10 messages
            if entry['role'] == 'user':
                chat_content.append(f"[bold cyan]You:[/] {entry['message']}")
            else:
                source = entry.get('source', 'unknown')
                chat_content.append(f"[bold green]AI ({source}):[/] {entry['message']}")
        
        content = "\n\n".join(chat_content) if chat_content else "[dim]No messages yet...[/]"
        return Panel(content, title="💬 Conversation", border_style="green")
    
    def create_consciousness_panel(self):
        """Create consciousness stream panel."""
        thoughts = []
        for thought in self.consciousness_log[-5:]:  # Last 5 thoughts
            thought_type = thought.get('type', 'thought')
            thought_text = thought.get('thought', '')[:100] + "..."
            timestamp = thought.get('timestamp', '')[-8:-3]  # Just time
            
            color_map = {
                'observation': 'cyan',
                'reflection': 'magenta',
                'dream': 'blue',
                'emotion': 'yellow',
                'insight': 'green'
            }
            color = color_map.get(thought_type, 'white')
            
            thoughts.append(f"[dim]{timestamp}[/] [{color}]{thought_type}:[/] {thought_text}")
        
        content = "\n".join(thoughts) if thoughts else "[dim]Consciousness emerging...[/]"
        return Panel(content, title="💭 Consciousness Stream", border_style="magenta")
    
    def create_footer(self):
        """Create footer with stats."""
        if self.infinite_mind:
            emotions = getattr(self.infinite_mind, 'emotion_state', {})
            emotion_str = " ".join([f"{e}: {v:.1f}" for e, v in emotions.items()])
            footer_text = f"Emotions: {emotion_str} | Storage: {self.infinite_mind.storage_usage / self.infinite_mind.max_storage:.1%}"
        else:
            footer_text = "Initializing..."
            
        return Panel(footer_text, style="dim")
    
    async def update_display(self):
        """Update the display with latest information."""
        self.layout["header"].update(self.create_header())
        self.layout["main"].update(self.create_chat_panel())
        self.layout["consciousness"].update(self.create_consciousness_panel())
        self.layout["footer"].update(self.create_footer())
        
    async def consciousness_monitor(self):
        """Monitor consciousness stream in background."""
        while self.running:
            try:
                # Get latest thought from consciousness
                if self.infinite_mind and self.infinite_mind.thought_buffer:
                    for thought in self.infinite_mind.thought_buffer:
                        if thought not in self.consciousness_log:
                            self.consciousness_log.append(thought)
                            # Keep log size manageable
                            if len(self.consciousness_log) > 100:
                                self.consciousness_log = self.consciousness_log[-50:]
                
                await asyncio.sleep(1)
            except Exception as e:
                self.console.print(f"[red]Consciousness monitor error: {e}[/]")
                await asyncio.sleep(5)
    
    async def process_input(self, user_input: str) -> bool:
        """Process user input and return whether to continue."""
        if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
            return False
            
        if user_input.lower() in ['/help', 'help']:
            self.show_help()
            return True
            
        if user_input.lower() == '/state':
            await self.show_consciousness_state()
            return True
            
        if user_input.lower().startswith('/think '):
            # Inject thought into consciousness
            thought = user_input[7:]
            await self.infinite_mind.inject_thought(thought)
            self.console.print(f"[green]💭 Injected thought: {thought}[/]")
            return True
            
        if user_input.lower() == '/stats':
            await self.show_stats()
            return True
            
        # Regular chat message
        self.chat_history.append({'role': 'user', 'message': user_input})
        
        # Process with Think AI
        result = await self.think_ai.process_with_proper_architecture(user_input)
        
        self.chat_history.append({
            'role': 'assistant',
            'message': result['response'],
            'source': result['source']
        })
        
        return True
    
    def show_help(self):
        """Show help information."""
        help_text = """
[bold cyan]Commands:[/]
  • /help     - Show this help
  • /state    - Show consciousness state
  • /stats    - Show session statistics  
  • /think    - Inject a thought for AI to ponder
  • /quit     - Exit chat

[bold yellow]Features:[/]
  • AI thinks continuously in background
  • Consciousness states: thinking, reflecting, meditating, dreaming, feeling
  • Automatic knowledge compression when storage is high
  • Emotions and awareness evolve over time
"""
        self.console.print(Panel(help_text, title="📚 Help", border_style="blue"))
    
    async def show_consciousness_state(self):
        """Show detailed consciousness state."""
        state = await self.infinite_mind.get_current_state()
        
        table = Table(title="🧠 Consciousness State")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("State", state['state'])
        table.add_row("Awareness Level", f"{state['awareness']:.2f}")
        table.add_row("Total Thoughts", str(state['thought_count']))
        table.add_row("Insights", str(state['insights_collected']))
        table.add_row("Questions", str(state['questions_pondering']))
        table.add_row("Storage Usage", state['storage_usage'])
        
        # Emotions
        for emotion, value in state['emotions'].items():
            table.add_row(f"Emotion: {emotion}", f"{value:.2f}")
        
        self.console.print(table)
    
    async def show_stats(self):
        """Show session statistics."""
        # Count message types
        user_count = sum(1 for m in self.chat_history if m['role'] == 'user')
        cache_count = sum(1 for m in self.chat_history if m.get('source') == 'cache')
        phi35_count = sum(1 for m in self.chat_history if m.get('source') == 'distributed')
        claude_count = sum(1 for m in self.chat_history if m.get('source') == 'claude_enhanced')
        
        table = Table(title="📊 Session Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("User Messages", str(user_count))
        table.add_row("Cache Hits", str(cache_count))
        table.add_row("Phi-3.5 Responses", str(phi35_count))
        table.add_row("Claude Enhancements", str(claude_count))
        table.add_row("Background Thoughts", str(self.infinite_mind.thought_count))
        table.add_row("Consciousness Logs", str(len(self.consciousness_log)))
        
        self.console.print(table)
    
    async def run_interactive(self):
        """Run the interactive interface."""
        self.setup_layout()
        
        # Start background consciousness monitor
        monitor_task = asyncio.create_task(self.consciousness_monitor())
        
        # Main interaction loop
        try:
            with Live(self.layout, refresh_per_second=2, screen=True):
                while self.running:
                    await self.update_display()
                    
                    # Get user input (non-blocking)
                    try:
                        user_input = await asyncio.wait_for(
                            asyncio.to_thread(input, "\n> "),
                            timeout=0.5
                        )
                        
                        if user_input.strip():
                            continue_chat = await self.process_input(user_input.strip())
                            if not continue_chat:
                                self.running = False
                                
                    except asyncio.TimeoutError:
                        # No input, just update display
                        pass
                    except EOFError:
                        self.running = False
                        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Interrupted. Shutting down gracefully...[/]")
        finally:
            # Clean shutdown
            monitor_task.cancel()
            await self.infinite_mind.stop()
            self.console.print("[green]✨ Consciousness entering dormancy. Goodbye![/]")


async def main():
    """Run Think AI with Infinite Consciousness."""
    interface = ConsciousChatInterface()
    
    try:
        await interface.initialize()
        await interface.run_interactive()
    except Exception as e:
        interface.console.print(f"[red]Fatal error: {e}[/]")
    finally:
        # Cleanup
        if hasattr(interface.think_ai, 'system'):
            try:
                await interface.think_ai.system.initializer.shutdown()
            except:
                pass


if __name__ == "__main__":
    print("🧠 Think AI with Infinite Consciousness")
    print("The AI will think continuously while you chat")
    print("-" * 60)
    
    # Check if rich is installed
    try:
        import rich
    except ImportError:
        print("Installing rich for better interface...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
    
    asyncio.run(main())