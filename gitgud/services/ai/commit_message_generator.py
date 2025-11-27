"""Generate commit messages using AI or heuristics."""

import re
from gitgud.types.git_types import GitStatus
from gitgud.services.ai.ollama import OllamaProvider


class CommitMessageGenerator:
    """Generate commit messages from diff analysis."""
    
    def __init__(self):
        """Initialize generator."""
        self.ollama = OllamaProvider()
    
    def generate(self, diff: str, status: GitStatus) -> str:
        """Generate commit message from diff.
        
        Args:
            diff: Git diff output
            status: Repository status
            
        Returns:
            Generated commit message or empty string if failed
        """
        # Try AI first
        if self.ollama.is_available():
            try:
                return self._generate_with_ai(diff, status)
            except Exception:
                pass
        
        # Fallback to heuristic
        return self._generate_heuristic(diff, status)
    
    def _generate_with_ai(self, diff: str, status: GitStatus) -> str:
        """Generate message using Ollama AI."""
        # Truncate diff if too long (Ollama has context limits)
        max_diff_length = 4000
        truncated_diff = diff[:max_diff_length]
        if len(diff) > max_diff_length:
            truncated_diff += "\n... (diff truncated)"
        
        prompt = self._build_prompt(truncated_diff, status)
        
        response = self._make_request(prompt)
        
        if response:
            # Extract just the commit message (AI might add extra text)
            message = self._clean_ai_response(response)
            return message
        
        return ""
    
    def _make_request(self, prompt: str) -> str:
        """Make request to Ollama."""
        import requests
        
        try:
            response = requests.post(
                f"{self.ollama.endpoint}/api/generate",
                json={
                    "model": self.ollama.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
        except Exception:
            pass
        
        return ""
    
    def _build_prompt(self, diff: str, status: GitStatus) -> str:
        """Build prompt for AI."""
        return f"""You are a Git commit message expert following Conventional Commits format.

Analyze this git diff and write a clear, concise commit message.

Repository state:
- Modified files: {status.modified}
- New files: {status.created}
- Deleted files: {status.deleted}

Diff:
{diff}

Write a commit message following this format:
<type>: <short description>

<optional detailed description>

Types: feat, fix, docs, style, refactor, test, chore

Rules:
- First line max 72 characters
- Use imperative mood ("add" not "added")
- Be specific about what changed
- Don't include diff content in message

Just write the commit message, nothing else."""
    
    def _clean_ai_response(self, response: str) -> str:
        """Clean up AI response to extract commit message."""
        # Remove common AI preambles
        response = re.sub(r'^(Here\'s|Here is|The commit message is).*?:', '', response, flags=re.IGNORECASE)
        
        # Remove markdown code fences (at start or end)
        response = re.sub(r'^```\w*\s*', '', response)
        response = re.sub(r'\s*```\s*$', '', response)
        
        # Remove any remaining triple backticks
        response = response.replace('```', '')
        
        # Take only the commit message part
        lines = [line.strip() for line in response.strip().split('\n')]
        
        # Filter out empty lines at start and end
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        
        return '\n'.join(lines)
    
    def _generate_heuristic(self, diff: str, status: GitStatus) -> str:
        """Generate basic message using heuristics."""
        # Analyze what changed
        has_new_files = status.created > 0
        has_modified = status.modified > 0
        has_deleted = status.deleted > 0
        
        # Check for common patterns in diff
        is_feature = self._looks_like_feature(diff)
        is_fix = self._looks_like_fix(diff)
        is_docs = self._looks_like_docs(diff, status)
        is_refactor = self._looks_like_refactor(diff)
        
        # Determine type
        if is_fix:
            commit_type = "fix"
            description = "resolve issues"
        elif is_feature:
            commit_type = "feat"
            description = "add new functionality"
        elif is_docs:
            commit_type = "docs"
            description = "update documentation"
        elif is_refactor:
            commit_type = "refactor"
            description = "improve code structure"
        elif has_new_files:
            commit_type = "feat"
            description = "add new files"
        else:
            commit_type = "chore"
            description = "update code"
        
        # Build message
        summary = f"{commit_type}: {description}"
        
        # Add details
        details = []
        if status.modified > 0:
            details.append(f"- Update {status.modified} file(s)")
        if status.created > 0:
            details.append(f"- Add {status.created} new file(s)")
        if status.deleted > 0:
            details.append(f"- Remove {status.deleted} file(s)")
        
        if details:
            return summary + "\n\n" + "\n".join(details)
        
        return summary
    
    def _looks_like_feature(self, diff: str) -> bool:
        """Check if changes look like a new feature."""
        feature_keywords = ['new', 'add', 'create', 'implement', 'feature']
        diff_lower = diff.lower()
        return any(keyword in diff_lower for keyword in feature_keywords)
    
    def _looks_like_fix(self, diff: str) -> bool:
        """Check if changes look like a bug fix."""
        fix_keywords = ['fix', 'bug', 'issue', 'error', 'correct', 'resolve']
        diff_lower = diff.lower()
        return any(keyword in diff_lower for keyword in fix_keywords)
    
    def _looks_like_docs(self, diff: str, status: GitStatus) -> bool:
        """Check if changes are documentation."""
        # Check file extensions
        doc_extensions = ['.md', '.txt', '.rst', 'README', 'CHANGELOG']
        
        # Simple heuristic: check if diff mentions doc files
        diff_lower = diff.lower()
        return any(ext.lower() in diff_lower for ext in doc_extensions)
    
    def _looks_like_refactor(self, diff: str) -> bool:
        """Check if changes look like refactoring."""
        refactor_keywords = ['refactor', 'restructure', 'reorganize', 'cleanup', 'improve']
        diff_lower = diff.lower()
        return any(keyword in diff_lower for keyword in refactor_keywords)

