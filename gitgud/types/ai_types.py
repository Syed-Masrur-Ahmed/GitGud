from dataclasses import dataclass
from typing import List, Literal

@dataclass
class GitContext:
    """Context for AI analysis."""
    local_branch: str
    remote_branch: str | None
    commits_ahead: int
    commits_behind: int
    uncommitted_changes: int
    staged_changes: int
    has_stash: bool
    is_divergent: bool
    conflicting_files: List[str]

@dataclass
class AIResponse:
    """AI analysis response."""
    strategy: Literal['push', 'pull-then-push', 'stash-pull-push', 'rebase', 'merge', 'manual']
    commands: List[str]
    reasoning: str
    risks: List[str]
    requires_manual_review: bool
    confidence: int