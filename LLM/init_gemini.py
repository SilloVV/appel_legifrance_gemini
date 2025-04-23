import os 
from dotenv import load_dotenv
from google import genai
from LLM.env_variable_loader import load_var_env
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Get the Google API key from environment variables
GEMINI_API_KEY = load_var_env("GEMINI_API_KEY")

def initialize_gemini(model: str,GOOGLE_API_KEY:Optional[str] = GEMINI_API_KEY) -> genai.Client:
    """
    Initialisez le modèle Gemini avec les paramètres spécifiés.
    """
    # Create a new instance of the ChatModel
    client = genai.Client(
        api_key=GEMINI_API_KEY)
    
    return client

if __name__ == "__main__":
    """Exemple d'utilisation de la fonction initialize_gemini."""
    model = "gemini-2.0-flash-001"
    input = "Hello, how are you?"
    client = initialize_gemini(model, max_output_tokens=100, temperature=0.1)
    response = client.models.generate_content(
        model=model,
        contents=input,
    )
    print(response.text)
    
    

