from dataclasses import dataclass
from typing import Optional, List

@dataclass
class GitStatus:
    """Repository status information."""
    current: Optional[str]
    tracking: Optional[str]
    ahead: int
    behind: int
    modified: int
    created: int
    deleted: int
    conflicted: List[str]
    is_clean: bool

@dataclass
class BranchInfo:
    """Branch information."""
    local: str
    remote: Optional[str]
    ahead: int
    behind: int
    is_divergent: bool