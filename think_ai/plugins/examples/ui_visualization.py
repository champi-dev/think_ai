"""Example UI visualization plugin for Think AI."""

from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

from think_ai.plugins.base import (
    UIComponentPlugin,
    PluginMetadata,
    PluginCapability,
    PluginContext,
    plugin_event
)
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, DataTable, Sparkline, Label
from textual.reactive import reactive


class VisualizationPlugin(UIComponentPlugin):
    """Knowledge visualization plugin for Think AI terminal UI."""
    
    METADATA = PluginMetadata(
        name="visualization",
        version="1.0.0",
        author="Think AI Community",
        description="Beautiful visualizations for knowledge insights",
        capabilities=[PluginCapability.UI_COMPONENT],
        dependencies=["textual", "rich"],
        love_aligned=True,
        ethical_review_passed=True,
        tags=["ui", "visualization", "charts", "analytics"]
    )
    
    def __init__(self, metadata: Optional[PluginMetadata] = None):
        super().__init__(metadata or self.METADATA)
        self.data_points: List[float] = []
        self.knowledge_stats: Dict[str, int] = {
            "total_items": 0,
            "queries_today": 0,
            "active_connections": 0,
            "love_score": 85
        }
        self.recent_queries: List[Dict[str, Any]] = []
    
    async def initialize(self, context: PluginContext) -> None:
        """Initialize visualization plugin."""
        await super().initialize(context)
        
        # Register for data events
        self.register_hook("knowledge_stored", self._update_stats)
        self.register_hook("query_executed", self._track_query)
        self.register_hook("love_metric_calculated", self._update_love_score)
        
        # Start background data collection
        asyncio.create_task(self._collect_metrics())
    
    def get_widget(self) -> Any:
        """Get the visualization widget."""
        return KnowledgeVisualizationWidget(self)
    
    async def handle_event(self, event: Dict[str, Any]) -> None:
        """Handle UI events."""
        event_type = event.get("type")
        
        if event_type == "refresh":
            await self._refresh_data()
        elif event_type == "export":
            await self._export_visualization(event.get("format", "png"))
        elif event_type == "filter":
            await self._apply_filter(event.get("filter"))
    
    async def _update_stats(self, data: Dict[str, Any]) -> None:
        """Update knowledge statistics."""
        self.knowledge_stats["total_items"] += 1
        
        # Track data points for sparkline
        self.data_points.append(float(len(data.get("content", ""))))
        if len(self.data_points) > 50:
            self.data_points.pop(0)
    
    async def _track_query(self, data: Dict[str, Any]) -> None:
        """Track query execution."""
        self.knowledge_stats["queries_today"] += 1
        
        query_info = {
            "query": data.get("query", ""),
            "timestamp": datetime.now(),
            "results": data.get("results_count", 0),
            "time_ms": data.get("processing_time_ms", 0)
        }
        
        self.recent_queries.append(query_info)
        if len(self.recent_queries) > 10:
            self.recent_queries.pop(0)
    
    async def _update_love_score(self, data: Dict[str, Any]) -> None:
        """Update love alignment score."""
        new_score = data.get("score", 85)
        # Smooth the score changes
        self.knowledge_stats["love_score"] = int(
            0.7 * self.knowledge_stats["love_score"] + 0.3 * new_score
        )
    
    async def _collect_metrics(self) -> None:
        """Background task to collect metrics."""
        while self._initialized:
            # Simulate active connections
            self.knowledge_stats["active_connections"] = len(
                self._context.engine.storage_backends
            ) if self._context else 0
            
            await asyncio.sleep(5)
    
    async def _refresh_data(self) -> None:
        """Refresh visualization data."""
        # Emit refresh event
        await self.emit_event("visualization_refresh", {
            "stats": self.knowledge_stats,
            "data_points": self.data_points
        })
    
    async def _export_visualization(self, format: str) -> None:
        """Export visualization."""
        # In production, this would generate actual export
        logger.info(f"Exporting visualization as {format}")
    
    async def _apply_filter(self, filter_config: Dict[str, Any]) -> None:
        """Apply visualization filter."""
        # Filter data based on config
        pass
    
    def get_chart_data(self) -> Dict[str, Any]:
        """Get data for charts."""
        return {
            "sparkline": self.data_points,
            "stats": self.knowledge_stats,
            "queries": self.recent_queries,
            "pie_data": self._calculate_category_distribution()
        }
    
    def _calculate_category_distribution(self) -> List[Dict[str, Any]]:
        """Calculate knowledge category distribution."""
        # In production, this would analyze actual data
        return [
            {"category": "Technical", "value": 35, "color": "cyan"},
            {"category": "Scientific", "value": 25, "color": "green"},
            {"category": "Cultural", "value": 20, "color": "yellow"},
            {"category": "Personal", "value": 15, "color": "magenta"},
            {"category": "Other", "value": 5, "color": "white"}
        ]
    
    async def health_check(self) -> Dict[str, Any]:
        """Check visualization plugin health."""
        health = await super().health_check()
        
        health["metrics_collected"] = len(self.data_points)
        health["active_visualizations"] = 1  # Could track multiple
        health["last_update"] = datetime.now().isoformat()
        
        return health


class KnowledgeVisualizationWidget(Container):
    """Textual widget for knowledge visualization."""
    
    def __init__(self, plugin: VisualizationPlugin):
        super().__init__()
        self.plugin = plugin
    
    def compose(self) -> ComposeResult:
        """Compose the visualization UI."""
        with Vertical():
            # Header
            yield Static("🧠 Knowledge Insights", classes="header")
            
            # Stats row
            with Horizontal(classes="stats-row"):
                yield self._create_stat_box("Total Knowledge", "total_items", "📚")
                yield self._create_stat_box("Queries Today", "queries_today", "🔍")
                yield self._create_stat_box("Active Sources", "active_connections", "🔗")
                yield self._create_stat_box("Love Score", "love_score", "💝", suffix="%")
            
            # Main visualization area
            with Horizontal(classes="viz-area"):
                # Sparkline chart
                with Vertical(classes="chart-container"):
                    yield Static("Activity Timeline", classes="chart-title")
                    yield Sparkline(
                        self.plugin.data_points,
                        id="activity-sparkline",
                        classes="sparkline"
                    )
                
                # Category distribution
                with Vertical(classes="chart-container"):
                    yield Static("Knowledge Categories", classes="chart-title")
                    yield self._create_pie_chart()
            
            # Recent queries table
            yield Static("Recent Queries", classes="section-title")
            yield self._create_queries_table()
            
            # Action buttons
            with Horizontal(classes="actions"):
                yield Button("Refresh", id="refresh-btn", variant="primary")
                yield Button("Export", id="export-btn")
                yield Button("Settings", id="settings-btn")
    
    def _create_stat_box(
        self,
        label: str,
        stat_key: str,
        icon: str,
        suffix: str = ""
    ) -> Container:
        """Create a statistics box."""
        value = self.plugin.knowledge_stats.get(stat_key, 0)
        
        return Container(
            Static(f"{icon} {label}", classes="stat-label"),
            Static(f"{value}{suffix}", classes="stat-value", id=f"stat-{stat_key}"),
            classes="stat-box"
        )
    
    def _create_pie_chart(self) -> Container:
        """Create a simple text-based pie chart."""
        data = self.plugin._calculate_category_distribution()
        
        with Vertical(classes="pie-chart"):
            for item in data:
                percentage = item["value"]
                bar_length = int(percentage / 5)  # Scale to fit
                bar = "█" * bar_length
                
                yield Static(
                    f"[{item['color']}]{bar}[/] {item['category']} ({percentage}%)",
                    classes="pie-segment"
                )
    
    def _create_queries_table(self) -> DataTable:
        """Create recent queries table."""
        table = DataTable(id="queries-table", classes="queries-table")
        
        # Add columns
        table.add_column("Time", width=10)
        table.add_column("Query", width=40)
        table.add_column("Results", width=10)
        table.add_column("Time (ms)", width=10)
        
        # Add rows
        for query in self.plugin.recent_queries[-5:]:  # Last 5 queries
            table.add_row(
                query["timestamp"].strftime("%H:%M:%S"),
                query["query"][:40] + "..." if len(query["query"]) > 40 else query["query"],
                str(query["results"]),
                str(query["time_ms"])
            )
        
        return table
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "refresh-btn":
            await self.plugin.handle_event({"type": "refresh"})
            self.refresh()
        elif button_id == "export-btn":
            await self.plugin.handle_event({"type": "export", "format": "png"})
        elif button_id == "settings-btn":
            # Show settings dialog
            pass
    
    def update_stats(self) -> None:
        """Update statistics display."""
        for stat_key, value in self.plugin.knowledge_stats.items():
            stat_widget = self.query_one(f"#stat-{stat_key}", Static)
            if stat_widget:
                suffix = "%" if stat_key == "love_score" else ""
                stat_widget.update(f"{value}{suffix}")
    
    def update_sparkline(self) -> None:
        """Update sparkline chart."""
        sparkline = self.query_one("#activity-sparkline", Sparkline)
        if sparkline:
            sparkline.data = self.plugin.data_points
    
    def on_mount(self) -> None:
        """Set up refresh timer when mounted."""
        self.set_interval(2, self.update_stats)
        self.set_interval(5, self.update_sparkline)


# Export plugin class
__plugin__ = VisualizationPlugin