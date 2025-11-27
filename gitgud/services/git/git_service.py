from git import Repo, InvalidGitRepositoryError
from pathlib import Path
from typing import Optional
from gitgud.types.git_types import GitStatus, BranchInfo

class GitService:
    """Service for Git operations."""
    
    def __init__(self, path: str = "."):
        """Initialize Git service.
        
        Args:
            path: Path to git repository (default: current directory)
        """
        self.path = Path(path)
        self.repo: Optional[Repo] = None
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize Git repository."""
        try:
            self.repo = Repo(self.path, search_parent_directories=True)
        except InvalidGitRepositoryError:
            self.repo = None
    
    def is_git_repository(self) -> bool:
        """Check if current directory is a git repository."""
        return self.repo is not None
    
    def get_status(self) -> Optional[GitStatus]:
        """Get repository status.
        
        Returns:
            GitStatus object or None if not a repo
        """
        if not self.repo:
            return None
        
        # Get current branch (handle detached HEAD)
        try:
            current_branch = self.repo.active_branch.name
        except TypeError:
            # Detached HEAD state
            current_branch = "HEAD (detached)"
        
        # Get tracking branch info
        tracking_name = None
        ahead = behind = 0
        
        try:
            if current_branch != "HEAD (detached)":
                tracking = self.repo.active_branch.tracking_branch()
                tracking_name = tracking.name if tracking else None
                
                # Get ahead/behind counts
                if tracking:
                    ahead = len(list(self.repo.iter_commits(f'{tracking.name}..HEAD')))
                    behind = len(list(self.repo.iter_commits(f'HEAD..{tracking.name}')))
        except Exception:
            # If anything fails, just use defaults
            pass
        
        # Get file changes
        try:
            modified = len([item for item in self.repo.index.diff(None)])
            created = len(self.repo.untracked_files)
            
            # Check for staged changes too
            staged = len(self.repo.index.diff("HEAD")) if self.repo.head.is_valid() else 0
            
            is_clean = (modified == 0 and created == 0 and staged == 0)
        except Exception:
            # Handle edge case of empty repo with no commits
            modified = created = staged = 0
            is_clean = True
        
        return GitStatus(
            current=current_branch,
            tracking=tracking_name,
            ahead=ahead,
            behind=behind,
            modified=modified,
            created=created,
            deleted=0,  # Not critical for MVP
            conflicted=[],  # Not critical for MVP
            is_clean=is_clean
        )
    
    def get_branch_info(self) -> Optional[BranchInfo]:
        """Get branch information.
        
        Returns:
            BranchInfo object or None if not a repo
        """
        status = self.get_status()
        if not status:
            return None
        
        return BranchInfo(
            local=status.current,
            remote=status.tracking,
            ahead=status.ahead,
            behind=status.behind,
            is_divergent=(status.ahead > 0 and status.behind > 0)
        )
    
    def fetch(self) -> bool:
        """Fetch from remote.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.repo:
            return False
        
        try:
            # Check if remote exists
            if not self.repo.remotes:
                # No remotes configured - this is OK for local-only repos
                return True
            
            self.repo.remotes.origin.fetch()
            return True
        except AttributeError:
            # No 'origin' remote - try first available remote
            if self.repo.remotes:
                self.repo.remotes[0].fetch()
            return True
        except Exception:
            # Network error, authentication error, etc.
            # Silent fail - we'll just work with local state
            return False
    
    def execute_command(self, command: str) -> bool:
        """Execute a git command.
        
        Args:
            command: Git command to execute (e.g., "git push origin main")
            
        Returns:
            True if successful, False otherwise
        """
        if not self.repo:
            return False
        
        try:
            # Parse command
            parts = command.strip().split()
            if parts[0] == "git":
                parts = parts[1:]  # Remove 'git' prefix
            
            if not parts:
                return False
            
            # Get the git command (e.g., 'stash', 'push', 'pull')
            git_command = parts[0]
            git_args = parts[1:]
            
            # Execute using GitPython's dynamic method calling
            # e.g., self.repo.git.stash() or self.repo.git.push('origin', 'main')
            git_method = getattr(self.repo.git, git_command)
            git_method(*git_args)
            return True
        except Exception as e:
            print(f"Command error: {e}")
            return False