from typing import Optional, Generator,Tuple, List, Any
# Pour charger les variables d'environnement
from .env_variable_loader import load_var_env

# Mistral AI
from langchain_mistralai import ChatMistralAI

#Variables utiles
MODEL_API_KEY_NAME=load_var_env("MISTRAL_API_KEY")


def initialize_mistral(model: str, max_output_tokens: int, temperature: float = 0.1, MODEL_API_KEY_NAME:Optional[str] = MODEL_API_KEY_NAME) -> None:
    """
    initlialise le modèle LLM
    """
    # La doc ChatMistralAI est dispo ici : https://docs.mistral.ai/api/#tag/chat/operation/chat_completion_v1_chat_completions_post
    llm = ChatMistralAI(
            model=model,
            temperature=temperature,
            max_tokens=max_output_tokens,
     )
    return llm

if __name__ == "__main__":
    # Exemple d'utilisation
    model = "mistral-large-latest"
    max_output_tokens = 100
    temperature = 0.1
    llm = initialize_mistral(model, max_output_tokens, temperature)
    print("LLM initialized successfully.")
    response = llm.invoke("Hello, how are you?")
    print(response.content)



