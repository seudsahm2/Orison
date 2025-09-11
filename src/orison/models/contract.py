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
    
    def conflicts_with(self, other: "Contract") -> bool:
        """Return True if this contract conflicts with the other.
            Minimal domain rule: a public 'keep canals clear' oath conflicts with any
            secret clause that implies blackwater dumping/discharge.
        """
        a = " ".join(self.clauses).lower()
        b = " ".join(other.clauses).lower()
        def mentions_clear(s: str) -> bool:
            return "keep canals clear" in s or "keep canal clear" in s
        def mentions_dump(s: str) -> bool:
            return "dump" in s or "discharge" in s or "blackwater" in s
        return (self.is_public and not other.is_public and mentions_clear(a) and mentions_dump(b)) or \
               (other.is_public and not self.is_public and mentions_clear(b) and mentions_dump(a))