import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIModel:
    def __init__(self):
        # Get token from environment variables
        self.token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not self.token:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable not set")
        self.client = InferenceClient(token=self.token)
        # Use a more reliable model for text generation
        self.model_name = os.getenv("HF_MODEL_NAME", "gpt2")

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the AI model based on the provided prompt.

        Args:
            prompt (str): The input prompt for the AI model

        Returns:
            str: The generated response from the AI model
        """
        try:
            # Using text generation with a more reliable model
            response = self.client.text_generation(
                prompt,
                model=self.model_name,
                max_new_tokens=150,
                temperature=0.7,
                do_sample=True,
                stop_sequences=["\nUser:", "\nAssistant:", "\nSystem:", "</s>"]
            )
            # Extract only the generated part, removing the original prompt
            if prompt in response:
                response = response[len(prompt):]
            return response.strip() if response.strip() else "AI could not generate a response."
        except Exception as e:
            # More detailed error handling
            print(f"AI Error: {str(e)}")
            # Try a fallback model if the primary one fails
            try:
                print("Trying fallback model...")
                response = self.client.text_generation(
                    prompt,
                    model="distilgpt2",  # Fallback to a more reliable model
                    max_new_tokens=150,
                    temperature=0.7,
                    do_sample=True,
                    stop_sequences=["\nUser:", "\nAssistant:", "\nSystem:", "</s>"]
                )
                if prompt in response:
                    response = response[len(prompt):]
                return response.strip() if response.strip() else "AI could not generate a response."
            except Exception as fallback_error:
                print(f"Fallback model also failed: {str(fallback_error)}")
                return f"AI is currently unavailable. Please try again later."

def get_ai_model():
    """
    Factory function to get an instance of the AI model.

    Returns:
        AIModel: An instance of the AI model
    """
    return AIModel()