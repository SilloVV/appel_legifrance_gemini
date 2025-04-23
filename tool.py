# -*- coding: utf-8 -*-
import json
from typing import Dict, List, Tuple, Any, Optional, Union

from LEGIFRANCE_UTILS.payload.payload_generator import create_payload
from LEGIFRANCE_UTILS.payload.parse_payload import parse_json_model_output
from SEARCH.search_call import search_call
from LEGIFRANCE_UTILS.display_article.get_article_from_id import print_article
from LEGIFRANCE_UTILS.synthetize.synthetize_response import synthesize_legal_response


def search_legifrance(question: str) -> Optional[str]:
    """
    Effectue une recherche dans la base de données Légifrance à partir d'une question juridique
    et retourne une synthèse des résultats.
    
    Args:
        question (str): La question juridique posée par l'utilisateur
        
    Returns:
        Optional[str]: La synthèse des résultats juridiques ou None en cas d'erreur
    """
    print(f"INFO: Traitement de la question: {question}")
    
    try:
        # Générer le payload pour la recherche
        payload = create_payload(user_input=question)
        print("INFO: Payload généré")
        
        # Convertir la chaîne en objet JSON
        json_payload = json.loads(payload)
        
        # Si un payload valide est détecté, appeler l'API Legifrance
        if not json_payload:
            print("ERREUR: Le payload JSON n'est pas valide.")
            return None
            
        # Appel de l'API Legifrance
        api_results, error = search_call(json_payload)
        
        # Vérification de l'erreur
        if error:
            print(f"ERREUR: {error}")
            return None
        
        if not api_results:
            print("INFO: Aucun résultat trouvé.")
            return "Aucun résultat juridique trouvé pour cette question."
        
        print(f"INFO: {len(api_results)} résultats trouvés.")
        
        # Préparation des métadonnées pour la synthèse
        metadata_list = []
        
        # Extraction des métadonnées à partir des résultats structurés
        for result in api_results:
            # Format standard pour tous les documents
            result_metadata = {
                "title": result["titles"][0]["title"] if result["titles"] else "Titre inconnu",
                "id": result["titles"][0]["id"] if result["titles"] else "",
                "cid": result["titles"][0]["cid"] if result["titles"] else "",
                "type": result["type"],
                "nature": result["nature"],
                "origin": result["origin"],
                "date": result["date"],
                "extracts": []
            }
            
            # Ajout des extraits pertinents
            for section in result["sections"]:
                for extract in section["extracts"]:
                    extract_data = {
                        "id": extract["id"],
                        "title": extract["title"] or extract["num"] or "Sans titre",
                        "section_title": section["title"],
                        "text": " ".join(extract["values"]) if extract["values"] else ""
                    }
                    result_metadata["extracts"].append(extract_data)
            
            metadata_list.append(result_metadata)
        
        # Génération de la synthèse
        synthesis = synthesize_legal_response(question, metadata_list)
        return synthesis
        
    except json.JSONDecodeError:
        print("ERREUR: Le LLM n'a pas généré de JSON valide pour l'appel à l'API.")
        return None
    except Exception as e:
        print(f"ERREUR: Exception lors de la recherche juridique: {str(e)}")
        return None


if __name__ == "__main__":
    # Exemple d'utilisation de la fonction search_legifrance
    user_question = input("Entrez votre question juridique : ")
    result = search_legifrance(user_question)
    
    if result:
        print("\n" + "=" * 80)
        print("RÉSULTAT DE LA RECHERCHE JURIDIQUE:")
        print("=" * 80)
        print(result)
        print("=" * 80)
    else:
        print("La recherche n'a pas pu aboutir. Veuillez réessayer avec une autre question.")