from typing import Optional
from gitgud.services.git.git_service import GitService
from gitgud.types.ai_types import GitContext

class ContextBuilder:
    """Build context for AI analysis from Git repository."""
    
    def __init__(self, git_service: GitService):
        """Initialize context builder.
        
        Args:
            git_service: Git service instance
        """
        self.git = git_service
    
    def build_context(self) -> Optional[GitContext]:
        """Build AI context from current repository state.
        
        Returns:
            GitContext or None if not a repository
        """
        if not self.git.is_git_repository():
            return None
        
        # Fetch latest from remote
        self.git.fetch()
        
        # Get status and branch info
        status = self.git.get_status()
        branch_info = self.git.get_branch_info()
        
        if not status or not branch_info:
            return None
        
        return GitContext(
            local_branch=branch_info.local,
            remote_branch=branch_info.remote,
            commits_ahead=branch_info.ahead,
            commits_behind=branch_info.behind,
            uncommitted_changes=status.modified + status.created + status.deleted,
            staged_changes=0,  # TODO: Calculate staged changes
            has_stash=False,  # TODO: Check for stash
            is_divergent=branch_info.is_divergent,
            conflicting_files=status.conflicted
        )