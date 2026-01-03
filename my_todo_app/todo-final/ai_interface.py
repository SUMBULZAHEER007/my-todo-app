# my_todo_app/ai_interface.py
import os
from abc import ABC, abstractmethod
from typing import List, Optional
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class AIModelInterface(ABC):
    """Abstract base class for AI models"""

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass

class OpenAIModel(AIModelInterface):
    """OpenAI model interface"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Using ChatOpenAI for better conversational capabilities
        self.model = ChatOpenAI(
            openai_api_key=api_key,
            model_name="gpt-3.5-turbo",  # Using a more cost-effective model
            temperature=0.7
        )

    def generate_response(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        try:
            response = self.model([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

class AnthropicModel(AIModelInterface):
    """Anthropic (Claude) model interface"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        from langchain.chat_models import ChatAnthropic
        self.model = ChatAnthropic(
            anthropic_api_key=api_key,
            model_name="claude-3-haiku-20240307",  # Using a more cost-effective model
            temperature=0.7
        )

    def generate_response(self, prompt: str) -> str:
        """Generate response using Anthropic (Claude)"""
        try:
            response = self.model([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

class LocalModel(AIModelInterface):
    """Local model interface using Ollama or similar"""

    def __init__(self):
        # For this implementation, we'll use a mock local model
        # In a real implementation, this would connect to Ollama or similar
        model_path = os.getenv("LOCAL_MODEL_PATH")
        if not model_path:
            # Using a simple mock for demonstration
            self.model = None
        else:
            # In a real implementation, we would load the local model
            from langchain.llms import LlamaCpp
            self.model = LlamaCpp(model_path=model_path)

    def generate_response(self, prompt: str) -> str:
        """Generate response using local model"""
        # For this implementation, we'll return a mock response
        # In a real implementation, this would call the local model
        if self.model:
            try:
                return self.model(prompt)
            except Exception as e:
                return f"Error generating response: {str(e)}"
        else:
            return f"Local model response to: {prompt[:50]}..."

def get_ai_model() -> AIModelInterface:
    """Factory function to get the appropriate AI model based on environment"""
    use_anthropic = os.getenv("USE_ANTHROPIC", "false").lower() == "true"
    use_local = os.getenv("USE_LOCAL_MODEL", "false").lower() == "true"

    if use_anthropic:
        return AnthropicModel()
    elif use_local:
        return LocalModel()
    else:
        return OpenAIModel()