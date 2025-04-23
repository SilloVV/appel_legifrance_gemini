from dotenv import load_dotenv
import os 

load_dotenv()

# pour réadapter le code en cas de besoin : outil de chargement de variable d'environnement centralisé (plus qu'à changer cela en cas de problème)
def load_var_env(VAR_NAME:str) -> str:
    """
	Charge la variable d'environnement depuis les variables d'environnement
	"""
    api_key = os.getenv(VAR_NAME)
    if api_key is None:
        raise ValueError(f"Environnement Variable {VAR_NAME} not found in environment variables.")
    return api_key




