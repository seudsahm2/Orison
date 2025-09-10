from typing import Protocol

class Arbiter(Protocol):
    def trade_memory_for_hint(self,memory: str) -> str:
        ...
        
class TerminalArbiter:
    def trade_memory_for_hint(self,memory: str) -> str:
        if not memory.strip():
            return "You must offer a real memory"
        if "canal" in memory.lower():
            return "The canals hide more than water. Check th ledger for missing report."
        if "dock" in memory.lower():
            return "The dock workers know about the blackwater. ask them again."
        return "Every memory is a clue. Look for what is missing"