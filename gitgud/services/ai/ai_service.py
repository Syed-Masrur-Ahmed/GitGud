from typing import List
from gitgud.types.ai_types import GitContext, AIResponse
from gitgud.services.ai.ollama import OllamaProvider
from gitgud.services.ai.heuristic import HeuristicProvider

class AIService:
    """AI service that orchestrates multiple providers."""
    
    def __init__(self, provider_type: str = "ollama"):
        """Initialize AI service.
        
        Args:
            provider_type: Type of provider to use ('ollama' or 'heuristic')
        """
        self.providers: List = []
        
        if provider_type == "ollama":
            self.providers.append(OllamaProvider())
        
        # Always add heuristic as fallback
        self.providers.append(HeuristicProvider())
    
    def analyze(self, context: GitContext) -> AIResponse:
        """Analyze context using available providers.
        
        Args:
            context: Git repository context
            
        Returns:
            AIResponse from first available provider
        """
        for provider in self.providers:
            try:
                if provider.is_available():
                    print(f"Using provider: {provider.__class__.__name__}")
                    return provider.analyze(context)
            except Exception as e:
                print(f"Provider {provider.__class__.__name__} failed: {e}")
                # Continue to next provider
        
        raise Exception("No AI provider available")