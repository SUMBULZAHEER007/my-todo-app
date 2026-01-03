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
        # Use a more appropriate model for text generation
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
            # Using a simpler approach that works better with gpt2 and similar models
            response = self.client.text_generation(
                prompt,
                model=self.model_name,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                stop_sequences=["\n\n", "</s>"]
            )
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
                    max_new_tokens=100,
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9,
                    stop_sequences=["\n\n", "</s>"]
                )
                return response.strip() if response.strip() else "AI could not generate a response."
            except Exception as fallback_error:
                print(f"Fallback model also failed: {str(fallback_error)}")
                return f"AI is thinking... please try again later."

    def categorize_task(self, description: str) -> str:
        """
        Categorize a task based on its description.
        Returns one of: 'Urgent', 'Work', 'Personal'
        """
        try:
            # Create a prompt specifically for task categorization
            prompt = f"Task: {description}\nCategory:"
            response = self.client.text_generation(
                prompt,
                model=self.model_name,
                max_new_tokens=10,  # Just need a short category response
                temperature=0.1,  # Lower temperature for more consistent results
                do_sample=False,  # Use greedy decoding for consistency
                stop_sequences=["\n", ".", " "]
            )

            # Process the response to extract the category
            category = response.strip().split()[-1].strip(" .,!?")

            # Normalize the category to match expected values
            category = category.capitalize()
            if category in ["Urgent", "Work", "Personal"]:
                return category
            else:
                # Default to Personal if the model returned something unexpected
                return "Personal"
        except Exception as e:
            print(f"Task categorization error: {str(e)}")
            # Default to Personal if AI categorization fails
            return "Personal"

def get_ai_model():
    """
    Factory function to get an instance of the AI model.

    Returns:
        AIModel: An instance of the AI model
    """
    return AIModel()