"""Main Terminal UI application using Textual."""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Input, Button, Static, DataTable, Label, Tree
from textual.binding import Binding
from textual.reactive import reactive
from textual import events
from textual.screen import Screen
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax
from datetime import datetime
import asyncio
from typing import Optional, List, Dict, Any

from ..core.engine import ThinkAIEngine
from ..core.config import Config
from ..utils.logging import get_logger


logger = get_logger(__name__)


class SearchResultWidget(Static):
    """Widget to display a search result."""
    
    def __init__(self, result: Dict[str, Any], index: int):
        super().__init__()
        self.result = result
        self.index = index
    
    def compose(self) -> ComposeResult:
        """Compose the search result display."""
        content = f"""[bold cyan]{self.index}. {self.result.get('key', 'Unknown')}[/bold cyan]
[dim]{self.result.get('created_at', 'No date')}[/dim]

{self.result.get('content', 'No content')}

[dim]Metadata: {self.result.get('metadata', {})}[/dim]"""
        
        yield Static(Panel(content, expand=True))


class QueryScreen(Screen):
    """Screen for querying knowledge."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("ctrl+s", "toggle_semantic", "Toggle Semantic Search"),
    ]
    
    def __init__(self, engine: ThinkAIEngine):
        super().__init__()
        self.engine = engine
        self.use_semantic = True
        self.results = []
    
    def compose(self) -> ComposeResult:
        """Create the query interface."""
        yield Header()
        
        with Container(id="query-container"):
            yield Label("Knowledge Query", id="query-title")
            
            with Horizontal(id="query-input-row"):
                yield Input(
                    placeholder="Enter your query (prefix: for prefix search)...",
                    id="query-input"
                )
                yield Button("Search", variant="primary", id="search-button")
            
            yield Label(f"Semantic Search: {'ON' if self.use_semantic else 'OFF'}", id="semantic-label")
            
            with ScrollableContainer(id="results-container"):
                yield Static("No results yet. Enter a query above.", id="results-placeholder")
        
        yield Footer()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "search-button":
            await self.perform_search()
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle enter key in input."""
        if event.input.id == "query-input":
            await self.perform_search()
    
    async def perform_search(self) -> None:
        """Execute the search query."""
        query_input = self.query_by_id("query-input", Input)
        query = query_input.value.strip()
        
        if not query:
            return
        
        # Show loading state
        results_container = self.query_one("#results-container", ScrollableContainer)
        results_container.remove_children()
        results_container.mount(Static("[yellow]Searching...[/yellow]"))
        
        try:
            # Perform search
            result = await self.engine.query_knowledge(
                query,
                limit=20,
                use_semantic_search=self.use_semantic
            )
            
            # Clear container
            results_container.remove_children()
            
            if result.results:
                # Display results
                results_container.mount(
                    Static(f"[green]Found {len(result.results)} results in {result.processing_time_ms:.1f}ms[/green]")
                )
                
                for i, item in enumerate(result.results, 1):
                    results_container.mount(SearchResultWidget(item, i))
            else:
                results_container.mount(Static("[red]No results found.[/red]"))
                
        except Exception as e:
            results_container.remove_children()
            results_container.mount(Static(f"[red]Error: {str(e)}[/red]"))
    
    def action_toggle_semantic(self) -> None:
        """Toggle semantic search on/off."""
        self.use_semantic = not self.use_semantic
        label = self.query_one("#semantic-label", Label)
        label.update(f"Semantic Search: {'ON' if self.use_semantic else 'OFF'}")


class StoreScreen(Screen):
    """Screen for storing knowledge."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("ctrl+s", "save_knowledge", "Save"),
    ]
    
    def __init__(self, engine: ThinkAIEngine):
        super().__init__()
        self.engine = engine
    
    def compose(self) -> ComposeResult:
        """Create the store interface."""
        yield Header()
        
        with Container(id="store-container"):
            yield Label("Store Knowledge", id="store-title")
            
            yield Label("Key:")
            yield Input(placeholder="unique-key-for-knowledge", id="key-input")
            
            yield Label("Content:")
            yield Input(
                placeholder="The content to store...",
                id="content-input"
            )
            
            yield Label("Metadata (JSON):")
            yield Input(
                placeholder='{"category": "example", "tags": ["tag1", "tag2"]}',
                id="metadata-input",
                value="{}"
            )
            
            with Horizontal(id="store-buttons"):
                yield Button("Save", variant="primary", id="save-button")
                yield Button("Clear", variant="warning", id="clear-button")
            
            yield Static("", id="store-status")
        
        yield Footer()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save-button":
            await self.save_knowledge()
        elif event.button.id == "clear-button":
            self.clear_form()
    
    async def save_knowledge(self) -> None:
        """Save the knowledge to the system."""
        key = self.query_one("#key-input", Input).value.strip()
        content = self.query_one("#content-input", Input).value.strip()
        metadata_str = self.query_one("#metadata-input", Input).value.strip()
        
        if not key or not content:
            self.update_status("[red]Key and content are required![/red]")
            return
        
        # Parse metadata
        try:
            import json
            metadata = json.loads(metadata_str) if metadata_str else {}
        except json.JSONDecodeError:
            self.update_status("[red]Invalid JSON metadata![/red]")
            return
        
        # Save knowledge
        try:
            item_id = await self.engine.store_knowledge(key, content, metadata)
            self.update_status(f"[green]✓ Saved successfully! ID: {item_id}[/green]")
            self.clear_form()
        except Exception as e:
            self.update_status(f"[red]Error: {str(e)}[/red]")
    
    def clear_form(self) -> None:
        """Clear all form inputs."""
        self.query_one("#key-input", Input).value = ""
        self.query_one("#content-input", Input).value = ""
        self.query_one("#metadata-input", Input).value = "{}"
        self.update_status("")
    
    def update_status(self, message: str) -> None:
        """Update the status message."""
        self.query_one("#store-status", Static).update(message)
    
    def action_save_knowledge(self) -> None:
        """Action to save knowledge (keyboard shortcut)."""
        asyncio.create_task(self.save_knowledge())


class StatsScreen(Screen):
    """Screen for viewing system statistics."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("r", "refresh", "Refresh"),
    ]
    
    def __init__(self, engine: ThinkAIEngine):
        super().__init__()
        self.engine = engine
    
    def compose(self) -> ComposeResult:
        """Create the stats interface."""
        yield Header()
        
        with Container(id="stats-container"):
            yield Label("System Statistics", id="stats-title")
            
            with Horizontal():
                yield Button("Refresh", variant="primary", id="refresh-button")
            
            yield Static("[yellow]Loading statistics...[/yellow]", id="stats-content")
        
        yield Footer()
    
    async def on_mount(self) -> None:
        """Load stats when screen mounts."""
        await self.load_stats()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "refresh-button":
            await self.load_stats()
    
    async def load_stats(self) -> None:
        """Load and display system statistics."""
        content = self.query_one("#stats-content", Static)
        content.update("[yellow]Loading statistics...[/yellow]")
        
        try:
            stats = await self.engine.get_system_stats()
            health = await self.engine.health_check()
            
            # Format statistics
            stats_text = f"""[bold cyan]System Status[/bold cyan]
Status: {'[green]Operational[/green]' if stats['status'] == 'operational' else '[red]Error[/red]'}
Version: {stats['config']['version']}
Health: {'[green]Healthy[/green]' if health['status'] == 'healthy' else '[red]Unhealthy[/red]'}

[bold cyan]Storage Statistics[/bold cyan]"""
            
            if 'storage' in stats and 'primary' in stats['storage']:
                primary = stats['storage']['primary']
                stats_text += f"""
Primary Storage (ScyllaDB):
  • Items: {primary.get('item_count', 'N/A')}
  • Backend: {primary.get('backend', 'N/A')}
  • Initialized: {'Yes' if primary.get('initialized') else 'No'}"""
            
            if 'storage' in stats and 'cache' in stats['storage']:
                cache = stats['storage']['cache']
                stats_text += f"""

Cache (Redis):
  • Memory Used: {cache.get('used_memory_human', 'N/A')}
  • Hit Rate: {cache.get('hit_rate', 0):.1f}%
  • Operations/sec: {cache.get('instantaneous_ops_per_sec', 0)}
  • Total Commands: {cache.get('total_commands_processed', 0):,}"""
            
            content.update(Panel(stats_text, title="System Statistics", expand=True))
            
        except Exception as e:
            content.update(f"[red]Error loading statistics: {str(e)}[/red]")
    
    def action_refresh(self) -> None:
        """Refresh statistics."""
        asyncio.create_task(self.load_stats())


class ThinkAIApp(App):
    """Main Think AI Terminal Application."""
    
    CSS = """
    #query-container, #store-container, #stats-container {
        padding: 1 2;
    }
    
    #query-title, #store-title, #stats-title {
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }
    
    #query-input-row {
        height: 3;
        margin-bottom: 1;
    }
    
    #query-input {
        width: 80%;
    }
    
    #search-button {
        width: 20%;
    }
    
    #results-container {
        height: 100%;
        border: solid $primary;
        padding: 1;
    }
    
    #store-buttons {
        margin-top: 1;
        height: 3;
    }
    
    #main-menu {
        align: center middle;
    }
    
    .menu-button {
        width: 30;
        margin: 1;
    }
    
    #semantic-label {
        color: $secondary;
        margin-bottom: 1;
    }
    
    #store-status {
        margin-top: 1;
    }
    
    SearchResultWidget {
        margin-bottom: 1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("h", "home", "Home"),
    ]
    
    def __init__(self, config: Optional[Config] = None):
        super().__init__()
        self.config = config or Config.from_env()
        self.engine = None
    
    def compose(self) -> ComposeResult:
        """Create the main application layout."""
        yield Header(show_clock=True)
        
        with Container(id="main-menu"):
            yield Label("Think AI - Universal Knowledge Access", id="app-title")
            yield Label("", classes="spacer")
            
            yield Button("🔍 Query Knowledge", variant="primary", classes="menu-button", id="query-button")
            yield Button("💾 Store Knowledge", variant="primary", classes="menu-button", id="store-button")
            yield Button("📊 System Stats", variant="primary", classes="menu-button", id="stats-button")
            yield Button("❌ Quit", variant="error", classes="menu-button", id="quit-button")
        
        yield Footer()
    
    async def on_mount(self) -> None:
        """Initialize the engine when app mounts."""
        self.engine = ThinkAIEngine(self.config)
        await self.engine.initialize()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle main menu button presses."""
        if event.button.id == "query-button":
            await self.push_screen(QueryScreen(self.engine))
        elif event.button.id == "store-button":
            await self.push_screen(StoreScreen(self.engine))
        elif event.button.id == "stats-button":
            await self.push_screen(StatsScreen(self.engine))
        elif event.button.id == "quit-button":
            self.exit()
    
    def action_home(self) -> None:
        """Return to home screen."""
        if len(self.screen_stack) > 1:
            self.pop_screen()
    
    async def on_unmount(self) -> None:
        """Cleanup when app closes."""
        if self.engine:
            await self.engine.shutdown()


def run_ui(config: Optional[Config] = None):
    """Run the Think AI Terminal UI."""
    app = ThinkAIApp(config)
    app.run()