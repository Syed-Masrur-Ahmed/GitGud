"""Generate commit messages using AI or heuristics."""

import re
import json
from gitgud.types.git_types import GitStatus
from gitgud.services.ai.ollama import OllamaProvider


class CommitMessageGenerator:
    """Generate commit messages from diff analysis."""
    
    def __init__(self, model: str = "llama3.2"):
        """Initialize generator.
        
        Args:
            model: Ollama model to use. Options:
                   - "llama3.2" (best for following instructions)
                   - "codellama:7b" (code focused but chatty)
                   - "mistral" (good balance)
        """
        self.ollama = OllamaProvider(model=model)
    
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
        max_diff_length = 3000
        truncated_diff = diff[:max_diff_length]
        if len(diff) > max_diff_length:
            truncated_diff += "\n... (truncated)"
        
        prompt = self._build_prompt(truncated_diff, status)
        
        response = self._make_request(prompt, use_json=True)
        
        if response:
            # Parse JSON response
            message = self._parse_json_response(response)
            if message:
                return message
            
            # If JSON parsing fails, try text parsing as fallback
            message = self._clean_ai_response(response)
            return message
        
        return ""
    
    def _make_request(self, prompt: str, use_json: bool = False) -> str:
        """Make request to Ollama."""
        import requests
        
        try:
            payload = {
                "model": self.ollama.model,
                "prompt": prompt,
                "stream": False,
            }
            
            # Request JSON format output (helps AI stay structured)
            if use_json:
                payload["format"] = "json"
            
            response = requests.post(
                f"{self.ollama.endpoint}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
        except Exception:
            pass
        
        return ""
    
    def _parse_json_response(self, response: str) -> str:
        """Parse JSON response from AI."""
        try:
            # Try to parse as JSON
            data = json.loads(response)
            
            # Extract type and message
            commit_type = data.get("type", "chore")
            commit_message = data.get("message", "")
            
            if commit_message:
                return f"{commit_type}: {commit_message}"
        except Exception:
            # Not valid JSON, return empty to try text parsing
            pass
        
        return ""
    
    def _build_prompt(self, diff: str, status: GitStatus) -> str:
        """Build prompt for AI."""
        return f"""Analyze these git changes and generate a commit message.

Files changed:
- Modified: {status.modified}
- New: {status.created}
- Deleted: {status.deleted}

Diff:
{diff}

Respond with ONLY a JSON object in this EXACT format:
{{
  "type": "feat",
  "message": "add user authentication system"
}}

Valid types: feat, fix, docs, style, refactor, test, chore

Rules:
- Be specific and descriptive
- Use imperative mood
- Keep message under 72 characters
- NO explanations, ONLY the JSON

Example output:
{{"type": "feat", "message": "implement OAuth2 authentication flow"}}"""
    
    def _clean_ai_response(self, response: str) -> str:
        """Clean up AI response to extract commit message."""
        # Remove markdown code fences
        response = re.sub(r'^```\w*\s*', '', response)
        response = re.sub(r'\s*```\s*$', '', response)
        response = response.replace('```', '')
        
        # Split into lines
        lines = [line.strip() for line in response.strip().split('\n')]
        
        # Remove empty lines at start
        while lines and not lines[0]:
            lines.pop(0)
        
        if not lines:
            return ""
        
        # Strategy: Take only the first line that looks like a commit message
        # and maybe bullet points that follow, but stop at explanatory text
        
        commit_lines = []
        found_commit_type = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # First line should be the commit message (type: description)
            if i == 0:
                # Check if it starts with a commit type
                if re.match(r'^(feat|fix|docs|style|refactor|test|chore|build|ci|perf):', line_lower):
                    commit_lines.append(line)
                    found_commit_type = True
                    continue
                else:
                    # Maybe AI didn't follow format, skip and try next line
                    continue
            
            # Stop at sentences explaining the commit message
            stop_phrases = [
                'this commit message',
                'this follows',
                'this meets',
                'the type of this',
                'which means that',
                'by outputting',
                'as requested',
                'as specified',
            ]
            
            if any(phrase in line_lower for phrase in stop_phrases):
                break
            
            # Only include bullet points or short continuation lines
            if line.startswith('-') and len(line) < 100:
                commit_lines.append(line)
            elif not line and commit_lines:  # Empty line after commit
                commit_lines.append(line)
            elif len(line) < 100 and not line.endswith('.') and i < 5:
                # Short continuation line (not a full sentence)
                commit_lines.append(line)
            else:
                # Stop at explanatory paragraphs
                break
        
        # Clean up trailing empty lines
        while commit_lines and not commit_lines[-1]:
            commit_lines.pop()
        
        result = '\n'.join(commit_lines)
        
        # If we got nothing useful, return first line that has content
        if not result and lines:
            return lines[0]
        
        return result
    
    def _generate_heuristic(self, diff: str, status: GitStatus) -> str:
        """Generate descriptive message using heuristics."""
        # Extract file names from diff
        file_names = self._extract_file_names(diff)
        
        # Extract added functions/classes for better context
        added_items = self._extract_added_items(diff)
        
        # Analyze what changed
        has_new_files = status.created > 0
        has_modified = status.modified > 0
        has_deleted = status.deleted > 0
        
        # Check for common patterns
        is_feature = self._looks_like_feature(diff)
        is_fix = self._looks_like_fix(diff)
        is_docs = self._looks_like_docs(diff, status)
        is_refactor = self._looks_like_refactor(diff)
        
        # Build descriptive message based on files and patterns
        commit_type = "chore"
        description = "update files"
        
        # Determine type and create specific description
        # For large changesets, be generic
        if len(file_names) > 50:
            commit_type = "chore"
            description = f"update {len(file_names)} files"
        
        # Check for new features first (before fix, since 'add' is common)
        elif is_feature or has_new_files:
            commit_type = "feat"
            
            # Prioritize function/class detection for most accurate description
            if added_items and len(added_items) >= 2:
                # Use actual code additions for description
                item_desc = ', '.join(added_items[:2])
                description = f"implement {item_desc}"
            elif added_items:
                # Single item
                description = f"implement {added_items[0]}"
            elif file_names:
                description = f"add {self._summarize_files(file_names)}"
            else:
                description = "add new functionality"
        
        elif is_fix:
            commit_type = "fix"
            # Try to extract what was fixed
            if 'bug' in diff.lower():
                description = "resolve bug"
            elif 'error' in diff.lower():
                description = "fix error handling"
            elif file_names:
                description = f"fix issues in {self._summarize_files(file_names)}"
            else:
                description = "resolve issues"
                
        elif is_docs:
            commit_type = "docs"
            if 'README' in diff:
                description = "update README"
            elif file_names:
                description = f"update {self._summarize_files(file_names)}"
            else:
                description = "update documentation"
                
        elif is_refactor:
            commit_type = "refactor"
            if file_names:
                description = f"refactor {self._summarize_files(file_names)}"
            else:
                description = "improve code structure"
                
        elif has_new_files:
            commit_type = "feat"
            description = f"add {self._summarize_files(file_names)}"
        
        else:
            # Try to infer from file names
            if file_names:
                description = f"update {self._summarize_files(file_names)}"
        
        # Build message
        summary = f"{commit_type}: {description}"
        
        # Add bullet points for context
        details = []
        
        # Add new functions/classes first (most informative)
        if added_items:
            for item in added_items:
                details.append(f"- add {item}")
        
        # Then add file information if useful
        elif len(file_names) > 1 and len(file_names) <= 5:
            for fname in file_names:
                action = "add" if has_new_files else "update"
                details.append(f"- {action} {fname}")
        elif len(file_names) > 5:
            details.append(f"- modify {len(file_names)} files")
        
        if details:
            return summary + "\n\n" + "\n".join(details)
        
        return summary
    
    def _extract_file_names(self, diff: str) -> list:
        """Extract file names from diff."""
        files = []
        
        # Get files from diff headers
        for line in diff.split('\n'):
            if line.startswith('diff --git'):
                # Extract filename: "diff --git a/file.py b/file.py"
                parts = line.split()
                if len(parts) >= 3:
                    fname = parts[2].replace('a/', '').replace('b/', '')
                    if fname and fname not in files:
                        files.append(fname)
        
        # Get untracked files (format: "  filename")
        if 'Untracked files:' in diff:
            in_untracked = False
            for line in diff.split('\n'):
                if 'Untracked files:' in line:
                    in_untracked = True
                    continue
                
                if in_untracked:
                    fname = line.strip()
                    
                    # Skip empty lines
                    if not fname:
                        continue
                    
                    # Skip lines that are clearly not filenames
                    if any(char in fname for char in ['(', ')', '{', '}', '[', ']', ':', ';']):
                        continue
                    
                    # Must look like a file path
                    if '/' in fname or '.' in fname:
                        if fname not in files:
                            files.append(fname)
                    else:
                        # Non-filename line = probably end of section
                        break
        
        return files
    
    def _summarize_files(self, files: list) -> str:
        """Create summary from file names."""
        if not files:
            return "files"
        
        if len(files) == 1:
            # Single file - use its name
            fname = files[0]
            # Remove extension and path
            base = fname.split('/')[-1].replace('.py', '').replace('.js', '').replace('.md', '')
            return base.replace('_', ' ')
        
        # Multiple files - find common pattern
        if all('.md' in f for f in files):
            return "documentation"
        elif all('.py' in f for f in files):
            return "Python modules"
        elif all('test' in f.lower() for f in files):
            return "tests"
        elif all('config' in f.lower() or 'setup' in f.lower() for f in files):
            return "configuration"
        else:
            return f"{len(files)} files"
    
    def _extract_added_items(self, diff: str) -> list:
        """Extract added functions, classes, etc. from diff."""
        items = []
        for line in diff.split('\n'):
            if not line.startswith('+'):
                continue
            
            line = line[1:].strip()  # Remove + and whitespace
            
            # Look for function/class definitions
            if line.startswith('def '):
                func_name = line.split('(')[0].replace('def ', '').strip()
                if func_name and not func_name.startswith('_'):  # Skip private
                    items.append(f"function {func_name}")
            elif line.startswith('class '):
                class_name = line.split(':')[0].replace('class ', '').split('(')[0].strip()
                if class_name:
                    items.append(f"class {class_name}")
            elif line.startswith('async def '):
                func_name = line.split('(')[0].replace('async def ', '').strip()
                if func_name and not func_name.startswith('_'):
                    items.append(f"async function {func_name}")
        
        return items[:3]  # Max 3 items
    
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

