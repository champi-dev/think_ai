"""
Lightweight UI and CLI library replacements
Minimal overhead terminal output with O(1) operations
"""

import sys
import time
from typing import Any, List, Optional, Union

class RichLite:
    """Minimal Rich console replacement"""
    
    class Console:
        def __init__(self, **kwargs):
            self.quiet = kwargs.get('quiet', False)
        
        def print(self, *args, **kwargs):
            """O(1) print operation"""
            if not self.quiet:
                print(*args)
        
        def log(self, *args, **kwargs):
            """O(1) log operation"""
            if not self.quiet:
                print(f"[LOG] {' '.join(str(a) for a in args)}")
        
        def rule(self, title="", **kwargs):
            """O(1) rule printing"""
            if not self.quiet:
                print(f"{'='*20} {title} {'='*20}")
        
        def status(self, message: str):
            """O(1) status context manager"""
            return StatusContext(message)
    
    class Panel:
        def __init__(self, content, title="", **kwargs):
            self.content = content
            self.title = title
        
        def __str__(self):
            return f"[{self.title}]\n{self.content}\n[/{self.title}]"
    
    class Table:
        def __init__(self, **kwargs):
            self.columns = []
            self.rows = []
        
        def add_column(self, name, **kwargs):
            self.columns.append(name)
        
        def add_row(self, *values):
            # O(1) - only store first row
            if not self.rows:
                self.rows.append(values)
        
        def __str__(self):
            if not self.columns:
                return ""
            header = " | ".join(self.columns)
            if self.rows:
                row = " | ".join(str(v) for v in self.rows[0])
                return f"{header}\n{row}"
            return header
    
    class Progress:
        def __init__(self, *args, **kwargs):
            self.tasks = {}
        
        def add_task(self, description: str, total: int = 100):
            task_id = len(self.tasks)
            self.tasks[task_id] = {"desc": description, "completed": 0, "total": total}
            return task_id
        
        def update(self, task_id: int, advance: int = 1, **kwargs):
            # O(1) update
            if task_id in self.tasks:
                self.tasks[task_id]["completed"] = min(
                    self.tasks[task_id]["completed"] + advance,
                    self.tasks[task_id]["total"]
                )
        
        def __enter__(self):
            return self
        
        def __exit__(self, *args):
            pass
    
    class Markdown:
        def __init__(self, text: str):
            self.text = text
        
        def __str__(self):
            return self.text
    
    @staticmethod
    def print(*args, **kwargs):
        print(*args)

class StatusContext:
    """Context manager for status messages"""
    
    def __init__(self, message: str):
        self.message = message
    
    def __enter__(self):
        print(f"[STATUS] {self.message}...")
        return self
    
    def __exit__(self, *args):
        print(f"[DONE] {self.message}")

class TextualLite:
    """Minimal Textual TUI framework replacement"""
    
    class App:
        def __init__(self, **kwargs):
            self.title = kwargs.get('title', 'App')
            self.widgets = []
        
        def compose(self):
            return self.widgets
        
        def run(self):
            print(f"=== {self.title} ===")
            print("(Lightweight TUI - press Ctrl+C to exit)")
            try:
                time.sleep(1)  # O(1) - instant "run"
            except KeyboardInterrupt:
                pass
        
        async def on_mount(self):
            pass
    
    class Widget:
        def __init__(self, content=""):
            self.content = content
        
        def __str__(self):
            return str(self.content)
    
    class Button(Widget):
        def __init__(self, label: str, **kwargs):
            super().__init__(f"[{label}]")
            self.on_click = kwargs.get('on_click')
    
    class Label(Widget):
        def __init__(self, text: str):
            super().__init__(text)
    
    class Input(Widget):
        def __init__(self, placeholder="", **kwargs):
            super().__init__(f"<{placeholder}>")

class TqdmLite:
    """Minimal tqdm progress bar replacement"""
    
    def __init__(self, iterable=None, desc=None, total=None, **kwargs):
        self.iterable = iterable
        self.desc = desc or ""
        self.total = total or (len(iterable) if hasattr(iterable, '__len__') else 100)
        self.n = 0
        self.disable = kwargs.get('disable', False)
    
    def __iter__(self):
        if self.iterable is None:
            return iter([])
        
        # O(1) - only show start and end
        if not self.disable:
            print(f"{self.desc}: Starting...")
        
        for item in self.iterable:
            yield item
            self.n += 1
            # Only update on first and last item
            if self.n == 1 or self.n == self.total:
                self.update(0)
        
        if not self.disable and self.n > 0:
            print(f"{self.desc}: Complete!")
    
    def update(self, n=1):
        """O(1) update - no-op for performance"""
        self.n += n
    
    def set_description(self, desc):
        """O(1) description update"""
        self.desc = desc
    
    def close(self):
        """O(1) close - no-op"""
        pass
    
    @classmethod
    def tqdm(cls, iterable=None, desc=None, **kwargs):
        return cls(iterable, desc, **kwargs)

# Click lightweight implementation
class ClickLite:
    """Minimal Click CLI framework replacement"""
    
    @staticmethod
    def command(name=None):
        def decorator(func):
            func._is_command = True
            func._name = name or func.__name__
            return func
        return decorator
    
    @staticmethod
    def option(*args, **kwargs):
        def decorator(func):
            # O(1) - just return the function
            return func
        return decorator
    
    @staticmethod
    def argument(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    @staticmethod
    def group(name=None):
        def decorator(func):
            func._is_group = True
            func._name = name or func.__name__
            return func
        return decorator
    
    @staticmethod
    def echo(message, **kwargs):
        print(message)
    
    @staticmethod
    def secho(message, **kwargs):
        # O(1) - ignore styling
        print(message)
    
    class Context:
        def __init__(self):
            self.obj = {}

# Colorama lightweight implementation  
class ColoramaLite:
    """Minimal colorama replacement"""
    
    class Fore:
        RED = ""
        GREEN = ""
        BLUE = ""
        YELLOW = ""
        CYAN = ""
        MAGENTA = ""
        WHITE = ""
        BLACK = ""
        RESET = ""
    
    class Back:
        RED = ""
        GREEN = ""
        BLUE = ""
        YELLOW = ""
        RESET = ""
    
    class Style:
        BRIGHT = ""
        DIM = ""
        NORMAL = ""
        RESET_ALL = ""
    
    @staticmethod
    def init(autoreset=True):
        """O(1) - no-op"""
        pass