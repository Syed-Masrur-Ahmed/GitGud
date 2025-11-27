from gitgud.types.ai_types import GitContext, AIResponse

class HeuristicProvider:
    """Rule-based decision making for Git operations."""
    
    def is_available(self) -> bool:
        """Always available."""
        return True
    
    def analyze(self, context: GitContext) -> AIResponse:
        """Analyze context and provide recommendation.
        
        Args:
            context: Git repository context
            
        Returns:
            AIResponse with recommendation
        """
        # Clean push scenario
        if (context.commits_ahead > 0 and 
            context.commits_behind == 0 and 
            context.uncommitted_changes == 0):
            return AIResponse(
                strategy='push',
                commands=['git push'],
                reasoning='Local branch is ahead of remote with no conflicts. Safe to push.',
                risks=[],
                requires_manual_review=False,
                confidence=95
            )
        
        # Need to pull first
        if (context.commits_behind > 0 and 
            not context.is_divergent and 
            context.uncommitted_changes == 0):
            return AIResponse(
                strategy='pull-then-push',
                commands=['git pull --rebase', 'git push'],
                reasoning='Remote has new commits. Pull with rebase to maintain linear history.',
                risks=['Rebase may cause conflicts that need manual resolution'],
                requires_manual_review=False,
                confidence=85
            )
        
        # Uncommitted changes + need to pull
        if context.commits_behind > 0 and context.uncommitted_changes > 0:
            return AIResponse(
                strategy='stash-pull-push',
                commands=['git stash', 'git pull --rebase', 'git stash pop', 'git push'],
                reasoning='Uncommitted changes need to be stashed before pulling.',
                risks=['Stash pop may cause conflicts', 'Rebase may cause conflicts'],
                requires_manual_review=False,
                confidence=75
            )
        
        # Divergent branches
        if context.is_divergent:
            return AIResponse(
                strategy='manual',
                commands=[],
                reasoning='Branches have diverged. Manual review required to choose between rebase, merge, or force push.',
                risks=['Force push will overwrite remote', 'Merge creates merge commit', 'Rebase rewrites history'],
                requires_manual_review=True,
                confidence=50
            )
        
        # Nothing to push - clean
        if context.commits_ahead == 0 and context.uncommitted_changes == 0:
            return AIResponse(
                strategy='manual',
                commands=[],
                reasoning='Nothing to push. Working tree is clean and up to date.',
                risks=[],
                requires_manual_review=False,
                confidence=100
            )
        
        # Uncommitted changes but nothing to push
        if context.commits_ahead == 0 and context.uncommitted_changes > 0:
            return AIResponse(
                strategy='manual',
                commands=[],
                reasoning='You have uncommitted changes but no commits to push. Commit your changes first with: git add . && git commit -m "your message"',
                risks=[],
                requires_manual_review=True,
                confidence=100
            )
        
        # Fallback
        return AIResponse(
            strategy='manual',
            commands=[],
            reasoning='Complex repository state detected. Manual review recommended.',
            risks=['Unable to determine safe automated approach'],
            requires_manual_review=True,
            confidence=30
        )