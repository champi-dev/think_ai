"""Lightweight tqdm implementation with O(1) operations."""

import sys
from typing import Any, Optional, Union, Iterable


class tqdm:
    """Minimal progress bar with O(1) updates."""
    
    def __init__(self, 
                 iterable: Optional[Iterable] = None,
                 desc: Optional[str] = None,
                 total: Optional[int] = None,
                 leave: bool = True,
                 file: Any = None,
                 ncols: Optional[int] = None,
                 mininterval: float = 0.1,
                 maxinterval: float = 10.0,
                 miniters: Optional[int] = None,
                 ascii: Optional[bool] = None,
                 disable: bool = False,
                 unit: str = 'it',
                 unit_scale: Union[bool, int, float] = False,
                 dynamic_ncols: bool = False,
                 smoothing: float = 0.3,
                 bar_format: Optional[str] = None,
                 initial: int = 0,
                 position: Optional[int] = None,
                 postfix: Optional[dict] = None,
                 unit_divisor: float = 1000,
                 **kwargs):
        
        self.iterable = iterable
        self.desc = desc or ''
        self.total = total
        self.leave = leave
        self.disable = disable
        self.n = initial
        self.pos = position or 0
        self._closed = False
        
    def __iter__(self):
        """O(1) iteration."""
        if self.iterable is None:
            return
            
        for obj in self.iterable:
            yield obj
            self.update(1)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, *args):
        """Context manager exit."""
        self.close()
    
    def update(self, n: int = 1):
        """O(1) progress update."""
        if self.disable or self._closed:
            return
        self.n += n
    
    def close(self):
        """O(1) cleanup."""
        if self._closed:
            return
        self._closed = True
    
    def set_description(self, desc: Optional[str] = None, refresh: bool = True):
        """O(1) description update."""
        self.desc = desc or ''
    
    def set_postfix(self, ordered_dict=None, refresh=True, **kwargs):
        """O(1) postfix update."""
        pass
    
    def refresh(self):
        """O(1) display refresh."""
        pass
    
    @classmethod
    def write(cls, s, file=None, end="\n", nolock=False):
        """O(1) write operation."""
        if file is None:
            file = sys.stdout
        file.write(s + end)
    
    def display(self, msg: Optional[str] = None, pos: Optional[int] = None):
        """O(1) display update."""
        pass


# Convenience functions
def trange(*args, **kwargs):
    """Shortcut for tqdm(range(*args), **kwargs)."""
    return tqdm(range(*args), **kwargs)