from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mark:
    """A simple token that proves witnessing or grants limited access.

    Level 6: @dataclass (fields, defaults)
    Level 4: __str__ vs __repr__ (human vs developer display)
    """
    id: str
    kind: str  # e.g., "witness", "seal", "archive"
    is_witness: bool = False
    
    def __str__(self) -> str:
        status = "witness" if self.is_witness else "token"
        return f"Mark[{self.id}] ({self.kind}, {status})"
    
