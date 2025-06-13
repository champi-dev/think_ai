from datetime import datetime, timedelta
import time

import json
from collections import defaultdict
from think_ai.plugins.base import (
from typing import Any, Dict, List

"""Example analytics plugin for Think AI."""

Plugin,
PluginCapability,
PluginContext,
PluginMetadata,
plugin_event,
)


class AnalyticsPlugin(Plugin):
"""Analytics plugin for tracking Think AI usage."""

    METADATA = PluginMetadata(
    name = "analytics",
    version = "1.0.0",
    author = "Think AI Community",
    description = "Usage analytics and insights for Think AI",
    capabilities = [PluginCapability.ANALYTICS],
    dependencies = [],
    love_aligned = True,
    ethical_review_passed = True,
    tags = ["analytics", "metrics", "insights"]
    )

    def __init__(self, metadata: Optional[PluginMetadata] = None):
        super().__init__(metadata or self.METADATA)
        self.metrics: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.counters: Dict[str, int] = defaultdict(int)
        self.love_metrics: Dict[str, float] = {
        "compassion_score": 0.0,
        "helpfulness_score": 0.0,
        "ethical_compliance": 0.0
        }

        async def initialize(self, context: PluginContext) - > None:
"""Initialize analytics plugin."""
            await super().initialize(context)

# Register for various events
            events_to_track = [
            "knowledge_stored",
            "knowledge_retrieved",
            "query_executed",
            "ethical_check_performed",
            "love_metric_calculated"
            ]

            for event in events_to_track:
                self.register_hook(event, self._track_event)

                async def shutdown(self) - > None:
"""Save analytics before shutdown."""
                    await self._save_analytics()
                    await super().shutdown()

                    @plugin_event("knowledge_stored")
                    async def track_storage(self, data: Dict[str, Any]) - > None:
"""Track knowledge storage events."""
                        self.counters["total_stored"] + = 1

                        self.metrics["storage"].append({
                        "timestamp": datetime.utcnow(),
                        "key": data.get("key"),
                        "size": len(str(data.get("content", ""))),
                        "has_metadata": bool(data.get("metadata"))
                        })

# Update love metrics if content was ethically enhanced
                        if data.get("ethically_enhanced"):
                            self.love_metrics["compassion_score"] + = 0.1

                            @plugin_event("query_executed")
                            async def track_query(self, data: Dict[str, Any]) - > None:
"""Track query execution."""
                                self.counters["total_queries"] + = 1

                                self.metrics["queries"].append({
                                "timestamp": datetime.utcnow(),
                                "query": data.get("query"),
                                "method": data.get("method"),
                                "results_count": data.get("results_count", 0),
                                "processing_time_ms": data.get("processing_time_ms", 0)
                                })

                                async def get_dashboard_stats(self) - > Dict[str, Any]:
"""Get statistics for dashboard display."""
                                    now = datetime.utcnow()
                                    hour_ago = now - timedelta(hours = 1)
                                    now - timedelta(days = 1)

# Calculate rates
                                    recent_storage = [
                                    m for m in self.metrics["storage"]
                                    if m["timestamp"] > hour_ago
                                    ]

                                    recent_queries = [
                                    m for m in self.metrics["queries"]
                                    if m["timestamp"] > hour_ago
                                    ]

                                    return {
                                "overview": {
                                "total_stored": self.counters["total_stored"],
                                "total_queries": self.counters["total_queries"],
                                "storage_rate_per_hour": len(recent_storage),
                                "query_rate_per_hour": len(recent_queries)
                                },
                                "performance": {
                                "avg_query_time_ms": self._calculate_avg_query_time(),
                                "cache_hit_rate": self._estimate_cache_hit_rate(),
                                "storage_success_rate": self._calculate_success_rate("storage")
                                },
                                "love_metrics": {
                                "overall_compassion": self.love_metrics["compassion_score"],
                                "helpfulness": self.love_metrics["helpfulness_score"],
                                "ethical_compliance": self.love_metrics["ethical_compliance"]
                                },
                                "recent_activity": {
                                "last_store": self._get_last_event("storage"),
                                "last_query": self._get_last_event("queries"),
                                "trending_queries": self._get_trending_queries()
                                }
                                }

                                async def generate_report(self, period: str = "daily") - > Dict[str, Any]:
"""Generate analytics report."""
                                    report = {
                                    "period": period,
                                    "generated_at": datetime.utcnow(),
                                    "summary": await self.get_dashboard_stats()
                                    }

# Add insights
                                    insights = []

# Performance insights
                                    avg_query_time = self._calculate_avg_query_time()
                                    if avg_query_time > 100:
                                        insights.append({
                                        "type": "performance",
                                        "message": "Query times are above 100ms. Consider optimizing indexes.",
                                        "severity": "warning"
                                        })

# Love metric insights
                                        if self.love_metrics["compassion_score"] < 0.5:
                                            insights.append({
                                            "type": "ethics",
                                            "message": "Compassion score is low. More content may need ethical enhancement.",
                                            "severity": "info"
                                            })

# Usage insights
                                            if self.counters["total_queries"] > self.counters["total_stored"] * 10:
                                                insights.append({
                                                "type": "usage",
                                                "message": "High read-to-write ratio. System is read-heavy.",
                                                "severity": "info"
                                                })

                                                report["insights"] = insights

                                                return report

                                            async def export_metrics(self, format: str = "json") - > str:
"""Export metrics in specified format."""
                                                if format = = "json":
                                                    return json.dumps({
                                                "metrics": dict(self.metrics),
                                                "counters": dict(self.counters),
                                                "love_metrics": self.love_metrics,
                                                "exported_at": datetime.utcnow().isoformat()
                                                }, default = str, indent = 2)

                                            elif format = = "csv":
# Simple CSV export of counters
                                                lines = ["metric,value"]
                                                for key, value in self.counters.items():
                                                    lines.append(f"{key},{value}")
                                                    return "\n".join(lines)

                                            else:
                                                raise ValueError(f"Unsupported format: {format}")

                                            async def _track_event(self, data: Dict[str, Any]) - > None:
"""Generic event tracking."""
                                                event_type = data.get("event_type", "unknown")
                                                self.counters[f"events_{event_type}"] + = 1

                                                async def _save_analytics(self) - > None:
"""Save analytics to persistent storage."""
# In production, this would save to a database or file
                                                    pass

                                                def _calculate_avg_query_time(self) - > float:
"""Calculate average query time."""
                                                    query_times = [
                                                    m["processing_time_ms"]
                                                    for m in self.metrics["queries"]
                                                    if "processing_time_ms" in m
                                                    ]

                                                    if not query_times:
                                                        return 0.0

                                                    return sum(query_times) / len(query_times)

                                                def _estimate_cache_hit_rate(self) - > float:
"""Estimate cache hit rate from query times."""
# Queries under 5ms likely hit cache
                                                    fast_queries = [
                                                    m for m in self.metrics["queries"]
                                                    if m.get("processing_time_ms", 0) < 5
                                                    ]

                                                    total_queries = len(self.metrics["queries"])
                                                    if total_queries = = 0:
                                                        return 0.0

                                                    return len(fast_queries) / total_queries

                                                def _calculate_success_rate(self, metric_type: str) - > float:
"""Calculate success rate for a metric type."""
# In production, track success / failure
                                                    return 0.95 # Placeholder

                                                def _get_last_event(self, metric_type: str) - > Optional[Dict[str, Any]]:
"""Get the last event of a type."""
                                                    events = self.metrics.get(metric_type, [])
                                                    if events:
                                                        return events[ - 1]
                                                    return None

                                                def _get_trending_queries(self, limit: int = 5) - > List[str]:
"""Get trending queries."""
# Count query frequencies
                                                    query_counts = defaultdict(int)

                                                    for metric in self.metrics["queries"]:
                                                        query = metric.get("query", "")
                                                        if query:
                                                            query_counts[query] + = 1

# Sort by frequency
                                                            trending = sorted(
                                                            query_counts.items(),
                                                            key = lambda x: x[1],
                                                            reverse = True
                                                            )

                                                            return [query for query, count in trending[:limit]]

                                                        async def health_check(self) - > Dict[str, Any]:
"""Check analytics plugin health."""
                                                            health = await super().health_check()

                                                            health["metrics_collected"] = sum(len(m) for m in self.metrics.values())
                                                            health["counters_tracked"] = len(self.counters)
                                                            health["love_metrics_active"] = any(v > 0 for v in self.love_metrics.values())

                                                            return health

# Export plugin class
                                                        __plugin__ = AnalyticsPlugin
