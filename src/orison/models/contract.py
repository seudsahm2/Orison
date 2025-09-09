from __future__ import annotations
from dataclasses import dataclass,field

@dataclass
class Contract:
    """A public or private agreement with simple clauses.

    Level 6: @dataclass with list field
    Level 4: __str__ vs __repr__ (user vs developer view)
    """
    id: str
    title: str
    clauses: list[str] = field(default_factory=list)
    is_public: bool = True
    
    def __str__(self) -> str:
        vis = "public" if self.is_public else "secret"
        parts = "; ".join(self.clauses) if self.clauses else "no clause"
        return f"Contract[{self.id}] {self.title} ({vis}) - {parts}"