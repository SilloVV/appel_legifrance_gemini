# initialisation du LLM 
from typing import Optional
from LLM.init_gemini import initialize_gemini

# variable environnement
from LLM.env_variable_loader import load_var_env
from dotenv import load_dotenv
import os 

# prompts
from Prompts.create_payload import system_prompt

# parser 
from LEGIFRANCE_UTILS.payload.parse_payload import parse_json_model_output

MODEL_NAME="gemini-2.0-flash-001"

# Initialiser le modèle LLM
llm = initialize_gemini(MODEL_NAME)

def create_payload(user_input:str,context:Optional[str] = None)->str:
    """
    Crée le payload pour l'appel API
    """
    
    # Créer les messages avec la structure appropriée
    messages = [
        {
            "role": "user",
            "parts": [
                {"text": user_input}
            ]
        }
    ]
    
    # Ajouter le system prompt comme premier message
    system_message = {
        "role": "model",
        "parts": [
            {"text": system_prompt}
        ]
    }
    messages.insert(0, system_message)
    
    # Si un contexte est fourni, l'ajouter aux messages
    if context:
        context_message = {
            "role": "model",  # ou "assistant" selon votre besoin
            "parts": [
                {"text": context}
            ]
        }
        messages.append(context_message)
    
    # Appeler l'API Gemini avec les messages formatés
    response = llm.models.generate_content(
        model=MODEL_NAME,
        contents=messages
    )
    
    # Traiter la réponse
    str_response = response.text
    payload = parse_json_model_output(str_response)
    
    return payload

if __name__ == "__main__":
    # Exemple d'utilisation de la fonction create_payload
    payload = create_payload()
    print(payload)
