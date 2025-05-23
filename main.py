# -*- coding: utf-8 -*-
import json
import os

from LEGIFRANCE_UTILS.payload.payload_generator import create_payload
from LEGIFRANCE_UTILS.payload.parse_payload import parse_json_model_output
from SEARCH.search_call import search_call, format_search_results
from LEGIFRANCE_UTILS.display_article.get_article_from_id import print_article
from LEGIFRANCE_UTILS.synthetize.synthetize_response import synthesize_legal_response


def main():
    # Le payload_generator demande déjà la question à l'utilisateur
    # Générer le payload pour la recherche
    user_input = input("Entrez votre question : ")
    

    payload = create_payload(user_input=user_input)
    print(f"INFO: Payload généré \n ")

    try:
        # Tenter de convertir la chaîne en objet JSON
        json_payload = json.loads(payload)
                
        # Si un payload valide est détecté, appeler l'API Legifrance
        if json_payload:
            # Appel de l'API une seule fois
            api_results, error = search_call(json_payload)
            
            # Vérification de l'erreur
            if error:
                print(f"Erreur: {error}")
                return
            
            if not api_results:
                print("Aucun résultat trouvé.\n")
                return
            
            #  affichage des documents formattés
            format_search_results(api_results)

            # Préparation des métadonnées pour la synthèse
            metadata_list = []
            
            # Extraction des métadonnées à partir des résultats structurés
            for result in api_results:
                    # Pour les autres documents, utiliser le format standard
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
            #print("\nSynthèse des résultats :")
            synthesis = synthesize_legal_response(user_input, metadata_list)
            print(synthesis)
        else:
            print("Le payload JSON n'est pas valide.")
                    
    except json.JSONDecodeError:
        print("Le LLM n'a pas généré de JSON valide pour l'appel à l'API.")
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API : {str(e)}")

if __name__ == "__main__":
    main()