"""Lightweight OpenTelemetry implementation with O(1) operations."""

from typing import Any, Dict, Optional, Callable
from contextlib import contextmanager


# Context module
class Context:
    """Lightweight context management."""
    
    def __init__(self):
        self._context = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """O(1) context retrieval."""
        return self._context.get(key, default)
    
    def set(self, key: str, value: Any):
        """O(1) context setting."""
        self._context[key] = value


# Trace module
class Span:
    """Lightweight span implementation."""
    
    def __init__(self, name: str, context: Optional[Context] = None):
        self.name = name
        self.context = context or Context()
        self.attributes = {}
        self.events = []
        self.status = "OK"
    
    def set_attribute(self, key: str, value: Any):
        """O(1) attribute setting."""
        self.attributes[key] = value
    
    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """O(1) event addition."""
        self.events.append({"name": name, "attributes": attributes or {}})
    
    def set_status(self, status: str):
        """O(1) status update."""
        self.status = status
    
    def end(self):
        """O(1) span end."""
        pass


class Tracer:
    """Lightweight tracer implementation."""
    
    def __init__(self, name: str = "default"):
        self.name = name
    
    @contextmanager
    def start_as_current_span(self, name: str, **kwargs):
        """O(1) span creation and management."""
        span = Span(name)
        try:
            yield span
        finally:
            span.end()
    
    def start_span(self, name: str, **kwargs) -> Span:
        """O(1) span start."""
        return Span(name)


class TracerProvider:
    """Lightweight tracer provider."""
    
    def __init__(self):
        self._tracers = {}
    
    def get_tracer(self, name: str, version: Optional[str] = None) -> Tracer:
        """O(1) tracer retrieval."""
        if name not in self._tracers:
            self._tracers[name] = Tracer(name)
        return self._tracers[name]


# Global tracer provider
_tracer_provider = TracerProvider()


def get_tracer(name: str, version: Optional[str] = None) -> Tracer:
    """O(1) global tracer retrieval."""
    return _tracer_provider.get_tracer(name, version)


def set_tracer_provider(provider: TracerProvider):
    """O(1) provider setting."""
    global _tracer_provider
    _tracer_provider = provider


# Metrics module  
class Counter:
    """Lightweight counter metric."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.value = 0
    
    def add(self, amount: int = 1, attributes: Optional[Dict[str, Any]] = None):
        """O(1) counter increment."""
        self.value += amount


class Histogram:
    """Lightweight histogram metric."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.count = 0
        self.sum = 0
    
    def record(self, value: float, attributes: Optional[Dict[str, Any]] = None):
        """O(1) value recording."""
        self.count += 1
        self.sum += value


class Meter:
    """Lightweight meter implementation."""
    
    def __init__(self, name: str = "default"):
        self.name = name
        self._instruments = {}
    
    def create_counter(self, name: str, description: str = "", **kwargs) -> Counter:
        """O(1) counter creation."""
        counter = Counter(name, description)
        self._instruments[name] = counter
        return counter
    
    def create_histogram(self, name: str, description: str = "", **kwargs) -> Histogram:
        """O(1) histogram creation."""
        histogram = Histogram(name, description)
        self._instruments[name] = histogram
        return histogram


class MeterProvider:
    """Lightweight meter provider."""
    
    def __init__(self):
        self._meters = {}
    
    def get_meter(self, name: str, version: Optional[str] = None) -> Meter:
        """O(1) meter retrieval."""
        if name not in self._meters:
            self._meters[name] = Meter(name)
        return self._meters[name]


# Global meter provider
_meter_provider = MeterProvider()


def get_meter(name: str, version: Optional[str] = None) -> Meter:
    """O(1) global meter retrieval."""
    return _meter_provider.get_meter(name, version)


def set_meter_provider(provider: MeterProvider):
    """O(1) provider setting."""
    global _meter_provider
    _meter_provider = provider


# Propagators
class TextMapPropagator:
    """Lightweight propagator."""
    
    def inject(self, carrier: Dict[str, Any], context: Optional[Context] = None):
        """O(1) context injection."""
        if context:
            carrier["trace_id"] = "lightweight-trace-123"
    
    def extract(self, carrier: Dict[str, Any]) -> Optional[Context]:
        """O(1) context extraction."""
        if "trace_id" in carrier:
            ctx = Context()
            ctx.set("trace_id", carrier["trace_id"])
            return ctx
        return None


# Baggage
class Baggage:
    """Lightweight baggage implementation."""
    
    @staticmethod
    def set_baggage(key: str, value: str, context: Optional[Context] = None) -> Context:
        """O(1) baggage setting."""
        ctx = context or Context()
        baggage = ctx.get("baggage", {})
        baggage[key] = value
        ctx.set("baggage", baggage)
        return ctx
    
    @staticmethod
    def get_baggage(key: str, context: Optional[Context] = None) -> Optional[str]:
        """O(1) baggage retrieval."""
        if context:
            baggage = context.get("baggage", {})
            return baggage.get(key)
        return None


# Main modules
trace = type("trace", (), {
    "get_tracer": get_tracer,
    "set_tracer_provider": set_tracer_provider,
    "Span": Span,
    "Tracer": Tracer,
    "TracerProvider": TracerProvider,
})()

metrics = type("metrics", (), {
    "get_meter": get_meter,
    "set_meter_provider": set_meter_provider,
    "Counter": Counter,
    "Histogram": Histogram,
    "Meter": Meter,
    "MeterProvider": MeterProvider,
})()

context = type("context", (), {
    "Context": Context,
})()

propagate = type("propagate", (), {
    "TextMapPropagator": TextMapPropagator,
})()

baggage = Baggage