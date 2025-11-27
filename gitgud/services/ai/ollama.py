import requests
import json
from typing import Optional
from gitgud.types.ai_types import GitContext, AIResponse

class OllamaProvider:
    """Ollama AI provider for intelligent Git recommendations."""
    
    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "codellama:7b"):
        """Initialize Ollama provider.
        
        Args:
            endpoint: Ollama API endpoint
            model: Model name to use
        """
        self.endpoint = endpoint
        self.model = model
    
    def is_available(self) -> bool:
        """Check if Ollama is available.
        
        Returns:
            True if Ollama is running, False otherwise
        """
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def analyze(self, context: GitContext) -> AIResponse:
        """Analyze context using Ollama AI.
        
        Args:
            context: Git repository context
            
        Returns:
            AIResponse with AI recommendation
        """
        prompt = self._build_prompt(context)
        
        try:
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama returned status {response.status_code}")
            
            result = response.json()
            ai_text = result.get("response", "")
            
            return self._parse_response(ai_text)
        
        except Exception as e:
            raise Exception(f"Ollama analysis failed: {e}")
    
    def _build_prompt(self, context: GitContext) -> str:
        """Build prompt for AI analysis."""
        return f"""You are a Git expert. Analyze this repository state and recommend the safest push strategy.

Repository State:
- Local Branch: {context.local_branch}
- Remote Branch: {context.remote_branch or 'none'}
- Commits Ahead: {context.commits_ahead}
- Commits Behind: {context.commits_behind}
- Uncommitted Changes: {context.uncommitted_changes}
- Staged Changes: {context.staged_changes}
- Has Stash: {context.has_stash}
- Branch Divergent: {context.is_divergent}
- Conflicting Files: {', '.join(context.conflicting_files) or 'none'}

Respond ONLY with valid JSON in this exact format:
{{
  "strategy": "push|pull-then-push|stash-pull-push|rebase|merge|manual",
  "commands": ["git command 1", "git command 2"],
  "reasoning": "Brief explanation",
  "risks": ["risk 1", "risk 2"],
  "requires_manual_review": true or false,
  "confidence": 0-100
}}"""
    
    def _parse_response(self, text: str) -> AIResponse:
        """Parse AI response JSON."""
        try:
            parsed = json.loads(text)
            
            if not all(k in parsed for k in ['strategy', 'commands', 'reasoning']):
                raise ValueError("Missing required fields")
            
            return AIResponse(
                strategy=parsed['strategy'],
                commands=parsed.get('commands', []),
                reasoning=parsed['reasoning'],
                risks=parsed.get('risks', []),
                requires_manual_review=parsed.get('requires_manual_review', False),
                confidence=parsed.get('confidence', 50)
            )
        except Exception as e:
            raise Exception(f"Failed to parse AI response: {e}")