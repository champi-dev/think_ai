"""Code analysis patterns for Think AI."""

import re
from typing import Dict

def load_patterns() -> Dict[str, re.Pattern]:
    """Load regex patterns for code analysis."""
    return {
        "class": re.compile(r'\bclass\s+\w+'),
        "function": re.compile(r'\bdef\s+\w+'),
        "async": re.compile(r'\basync\s+def\s+\w+'),
        "import": re.compile(r'^import\s+\w+'),
        "from_import": re.compile(r'^from\s+\w+\s+import'),
        "variable": re.compile(r'\w+\s*=\s*.+'),
        "api_route": re.compile(r'@app\.\w+\([\'"].*[\'"]\)'),
        "decorator": re.compile(r'@\w+'),
        "type_hint": re.compile(r':\s*\w+'),
        "return_type": re.compile(r'->\s*\w+'),
    }