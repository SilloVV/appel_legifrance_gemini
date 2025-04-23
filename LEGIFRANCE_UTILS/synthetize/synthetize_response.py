"""
Module pour synthétiser les réponses à partir des documents juridiques.

Ce module fournit une fonction unique pour:
- Traiter les métadonnées des documents JURI récupérés
- Générer une synthèse cohérente en réponse à une question juridique
- Utiliser le modèle Gemini pour formuler des réponses précises
"""
from typing import Dict, List, Any
from LLM.init_gemini import initialize_gemini


# Variable pour contrôler les limites du prompt

MAX_TEXT_LENGTH = 3000  # Longueur maximale du texte par document

MODEL_NAME = "gemini-2.0-flash-001"

# Initialiser le modèle LLM
llm = initialize_gemini(MODEL_NAME)

def synthesize_legal_response(question: str, metadata_list: List[Dict[str, Any]]) -> str:
    """
    Fonction unique qui synthétise une réponse juridique à partir des métadonnées des documents
    
    Args:
        question (str): La question juridique posée par l'utilisateur
        metadata_list (List[Dict[str, Any]]): Liste des métadonnées des documents JURI
    
    Returns:
        str: La réponse synthétisée par le LLM
    """
    # Vérification des entrées
    if not metadata_list or len(metadata_list) == 0:
        return "Aucun document juridique trouvé pour répondre à cette question."
    
    # Filtrer les métadonnées avec erreur
    valid_metadata = [meta for meta in metadata_list if "error" not in meta]
    
    # Vérifier si des métadonnées valides ont été récupérées
    if not valid_metadata:
        return "Aucun document juridique valide trouvé parmi les documents fournis."
    
    # Limiter à un maximum de documents pour éviter de surcharger le contexte
    
    metadata_list = valid_metadata
    
    # Construction du prompt pour le LLM
    system_prompt = """Tu es un assistant juridique spécialisé qui fournit des réponses précises et factuelles.
Ton rôle est d'analyser attentivement les documents juridiques fournis pour répondre à la question posée.

IMPORTANT: Les documents contiennent les extraits dans la clé extract. 
C'est là que se trouve l'information substantielle dont tu as besoin.

INSTRUCTIONS D'ANALYSE ET DE RÉPONSE:

1. ANALYSE DES DOCUMENTS:
   - Vérifie si les documents contiennent une DÉFINITION EXPLICITE ou des ÉLÉMENTS CONSTITUTIFS précis du concept juridique demandé.
   - De simples mentions ou références indirectes ne sont PAS suffisantes pour considérer que les documents définissent le concept.
   - Si les documents ne contiennent pas de définition explicite du concept juridique demandé, tu ne dois PAS essayer d'en extraire une définition artificielle.

2. FORMULATION DE LA RÉPONSE:
   - Commence toujours ta réponse par "## RÉPONSE :"
   - utilise toutes les informations pertinentes des documents pour répondre à la question.
   - Si les documents contiennent une définition explicite du concept demandé, base ta réponse principalement sur ces informations avec citations précises.
   - Si les documents ne contiennent PAS de définition explicite, réponds DIRECTEMENT à la question en utilisant tes connaissances juridiques générales SANS JAMAIS mentionner l'insuffisance des documents ni faire référence à leur contenu.
   - Structure ta réponse de la façon suivante:
      * D'abord une définition générale claire et concise du concept juridique (sans dire que les documents ne le définissent pas)
      * Ensuite, sous le titre en gras "**Éléments constitutifs :**", liste les éléments essentiels avec des puces (*)
      * Si pertinent, ajoute sous le titre en gras "**Aspects spécifiques :**" jusqu'à 2 aspects spécifiques concernant le même sujetmaximum avec des puces (*)

3. CITATIONS ET SOURCES:
   - Pour chaque élément tiré des documents, cite textuellement les passages pertinents entre guillemets.
   - Termine toujours ta réponse par "## SOURCES:" suivi de:
      * Merci d'indiquer la source du document en allant au niveau de détail le plus précis possible :
        - Si vous ne disposez que du titre du texte, indiquez uniquement celui-ci
        - Si vous disposez du titre du texte et du chapitre, indiquez les deux
        - Si vous disposez du titre du texte, du chapitre et de l'article/extrait, indiquez les trois éléments
        - N'oubliez pas d'inclure les références précises des articles (par exemple Article L.123-45) si elles sont disponibles  
      * Si tu as utilisé uniquement tes connaissances générales: "Connaissances juridiques générales" et "#documents insuffisants"
   - Si les documents fournis étaient insuffisants pour répondre à la question, ajoute une ligne supplémentaire après les sources écrivant exactement: "# Documents insuffisants"

IMPORTANT: Ne commence JAMAIS ta réponse par "Les documents fournis ne contiennent pas" ou toute autre formulation signalant l'insuffisance des documents. Réponds directement à la question avec tes connaissances juridiques si les documents sont insuffisants.
"""
    
    user_prompt = f"""Question: {question}

Voici les documents juridiques pertinents:

"""
    
    # Formater les métadonnées pour le prompt
    for i, metadata in enumerate(metadata_list, 1):
        user_prompt += f"\n--- DOCUMENT {i} ---\n"
        
        # Ajouter d'abord les métadonnées descriptives
        meta_descriptives = {k: v for k, v in metadata.items() if k != "texte"}
        for key, value in meta_descriptives.items():
            user_prompt += f"{key}: {value}\n"
        
        # Ajouter ensuite le texte avec une indication claire
        if "texte" in metadata and metadata["texte"]:
            text_content = metadata["texte"]
            
            # Limiter le texte pour éviter de dépasser les limites du contexte
            if len(text_content) > MAX_TEXT_LENGTH:
                text_content = text_content[:MAX_TEXT_LENGTH] + "..."
                
            user_prompt += f"\nCONTENU DU DOCUMENT:\n{text_content}\n"
        else:
            user_prompt += "\nAucun contenu textuel disponible pour ce document.\n"
            
        user_prompt += "\n" + "-" * 50 + "\n"
    
    user_prompt += f"\nEn te basant sur ces documents juridiques, réponds à la question: {question}"
    
    # Créer les messages pour l'appel au LLM
    messages = [
        {
            "role": "model",
            "parts": [{"text": system_prompt}]
        },
        {
            "role": "user", 
            "parts": [{"text": user_prompt}]
        }
    ]
    
    # Appeler l'API Gemini avec les messages formatés
    try:
        response = llm.models.generate_content(
            model=MODEL_NAME,
            contents=messages
        )
        return response.text
    except Exception as e:
        print(f"Erreur lors de l'appel au LLM: {e}")
        return f"Impossible de générer une synthèse. Erreur: {str(e)}"


if __name__ == "__main__":
    # Exemple d'utilisation
    test_question = "Quels sont les droits d'un locataire en cas de préavis réduit?"
    
    # Exemple de métadonnées de document (simplifié pour l'exemple)
    test_metadata = [
        {
            "document_id": "JURITEXT000012345678",
            "origine": "JURI",
            "titre": "Arrêt de la Cour d'appel de Paris sur le préavis de location",
            "juridiction": "Cour d'appel de Paris",
            "etat": "Actif",
            "date_debut": "2023-01-15",
            "date_fin": "",
            "texte": "Le préavis applicable au congé délivré par le locataire peut être réduit à un mois dans plusieurs situations..."
        }
    ]
    
    response = synthesize_legal_response(test_question, test_metadata)
    print(response)