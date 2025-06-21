"""Base code generator functionality."""

from typing import Dict, Any
from .templates import PYTHON_TEMPLATES, WEB_TEMPLATES


class CodeGeneratorBase:
    """Base code generator with template support."""
    
    def __init__(self):
        """Initialize code generator."""
        self.templates = {}
        self.templates.update(PYTHON_TEMPLATES)
        self.templates.update(WEB_TEMPLATES)
        self.generated_count = 0
        
    def generate(self, description: str) -> str:
        """Generate code from description."""
        # Simple implementation for now
        self.generated_count += 1
        return f"# Generated code #{self.generated_count}"
        
    def get_template(self, template_type: str) -> str:
        """Get a specific template."""
        return self.templates.get(template_type, "")
        
    def add_template(self, name: str, template: str):
        """Add a new template."""
        self.templates[name] = template