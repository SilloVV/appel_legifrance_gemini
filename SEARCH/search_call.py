import requests
from typing import Dict, List, Tuple, Any, Optional
import json

# utilitaire api legifrance
from LEGIFRANCE_UTILS.legifrance_init import obtain_legifrance_token


# Configuration des identifiants API Legifrance Sandbox
LEGIFRANCE_BASE_URL = "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app"

# outil Langchain d'appel à l'endpoint search legifrance
def search_call(Payload: dict) -> Tuple[List[dict], str]:
    """
    Appel à l'endpoint /search de l'api Legifrance
    
    Args:
        Payload (dict): Le payload de recherche à envoyer à l'API
        
    Returns:
        Tuple[List[dict], str]: 
            - Liste de dictionnaires contenant les informations détaillées des résultats
            - Message d'erreur en cas d'échec ou chaîne vide si succès
    """
    token = obtain_legifrance_token()
    
    if not token:
        return [], "Échec de connexion à Legifrance (échec d'obtention du token)"
    
    # Headers pour l'API
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    # Test de connexion à l'API
    pong = requests.get(f"{LEGIFRANCE_BASE_URL}/search/ping", headers=headers)

    if pong.status_code == 500:
        print("INFO: L'API Legifrance connectée !")
    else:
        return [], "ERREUR: L'API Legifrance ne répond pas."
    
    # Appel à l'API de recherche
    response = requests.post(f"{LEGIFRANCE_BASE_URL}/search", headers=headers, json=Payload)
    
    if response.status_code == 200:
        resultats = response.json()
        
        # Sauvegarde des résultats bruts dans un fichier JSON
        with open("resultats_legifrance.json", "w", encoding="utf-8") as file:
            json.dump(resultats, file, ensure_ascii=False, indent=4)
        
        # Vérification de la présence de résultats
        if resultats.get('results') is None:
            print("INFO: Aucun résultat trouvé.")
            return [], "Aucun résultat trouvé"
        
        # Liste pour stocker les résultats détaillés
        results_details = []
        
        for resultat in resultats.get('results', []):
            #print("INFO: Résultats trouvés !")
            
            # Informations de base du document
            doc_info = {
                "titles": [],
                "type": resultat.get('type'),
                "nature": resultat.get('nature'),
                "origin": resultat.get('origin'),
                "date": resultat.get('date'),
                "sections": []
            }
            
            # Extraction des titres
            for titre in resultat.get('titles', []):
                doc_info["titles"].append({
                    "title": titre.get('title', 'Titre non disponible'),
                    "cid": titre.get('cid', 'CID non disponible'),
                    "id": titre.get('id', 'ID non disponible')
                })
            
            # Extraction des sections et de leurs extraits
            for section in resultat.get('sections', []):
                section_info = {
                    "id": section.get('id'),
                    "title": section.get('title', 'Titre de section non disponible'),
                    "dateVersion": section.get('dateVersion'),
                    "legalStatus": section.get('legalStatus'),
                    "extracts": []
                }
                
                # Extraction des extraits de la section
                for extract in section.get('extracts', []):
                    extract_info = {
                        "id": extract.get('id'),
                        "title": extract.get('title', 'Titre d\'extrait non disponible'),
                        "num": extract.get('num'),
                        "legalStatus": extract.get('legalStatus'),
                        "values": extract.get('values', [])
                    }
                    section_info["extracts"].append(extract_info)
                
                doc_info["sections"].append(section_info)
            
            results_details.append(doc_info)
        
        print("INFO: Requête réussie !")
        return results_details, ""
    else:
        error_msg = f"Échec de la requête à Legifrance: code {response.status_code}"
        print(f"Erreur lors de la requête: {response.status_code} - {response.text}")
        return [], error_msg


def format_search_results(results: List[dict]) -> None:
    """
    Affiche les résultats de recherche de manière formatée
    
    Args:
        results (List[dict]): Liste des résultats de recherche
    """
    if not results:
        print("Aucun résultat à afficher.")
        return
    
    print("\n===== RÉSULTATS DE LA RECHERCHE =====\n")
    
    for i, result in enumerate(results, 1):
        print(f"DOCUMENT {i}:")
        
        # Affichage des titres du document
        for title in result["titles"]:
            print(f"  Titre: {title['title']}")
            print(f"  CID: {title['cid']}")
            print(f"  ID: {title['id']}")
        
        print(f"  Type: {result['type']}")
        print(f"  Nature: {result['nature']}")
        print(f"  Origine: {result['origin']}")
        print(f"  Date: {result['date']}")
        
        # Affichage des sections et de leurs extraits
        print("\n  SECTIONS:")
        for section in result["sections"]:
            print(f"    → {section['title']} (ID: {section['id']})")
            print(f"      Date de version: {section['dateVersion']}")
            print(f"      Statut légal: {section['legalStatus']}")
            
            # Affichage des extraits
            print("\n      EXTRAITS:")
            for extract in section["extracts"]:
                print(f"        · Extrait: {extract['title'] or extract['num'] or 'Sans titre'} (ID: {extract['id']})")
                print(f"          Statut légal: {extract['legalStatus']}")
                
                # Affichage des valeurs (texte des extraits)
                if extract["values"]:
                    print("          Texte:")
                    for value in extract["values"]:            
                        print(f"            {value}")
            
            print()  # Ligne vide entre les sections
        
        print("-" * 80)  # Séparateur entre les documents


## exemple d'utilisation de l'outil
if __name__ == "__main__":
    results, error = search_call(
        {
  "recherche": {
    "champs": [
      {
        "typeChamp": "ARTICLE",
        "criteres": [
          {
            "typeRecherche": "TOUS_LES_MOTS_DANS_UN_CHAMP",
            "valeur": "statut variable",
            "operateur": "ET",
            "proximité": 5
          },
          
        ],
        "operateur": "ET"
      }
    ],
    "pageNumber": 1,
    "pageSize": 8,
    "sort": "PERTINENCE"
  },
  "fond": "ALL"
}
        
           )
    
    if error:
        print(f"Erreur: {error}")
    else:
        doc  = format_search_results(results)