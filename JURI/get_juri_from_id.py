"""
Module pour récupérer et traiter les documents jurisprudentiels (JURI) depuis l'API Legifrance.

Ce module fournit des fonctions pour:
- Interroger l'API Legifrance et récupérer des documents JURI par leur identifiant
- Extraire différentes métadonnées des documents JURI (titre, juridiction, état, texte)
- Extraire les dates de début et de fin du document
- Afficher les informations de manière structurée

Les documents JURI sont des décisions de justice disponibles dans la base de données Legifrance.
"""
import requests
import datetime
import time
from typing import Dict, Optional, Union, Tuple, Any

# Pour récupérer le token d'authentification
from LEGIFRANCE_UTILS.legifrance_init import obtain_legifrance_token

# Configuration des URLs d'API
LEGIFRANCE_BASE_URL = "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app"
LEGIFRANCE_PROD_URL = "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app"

# Types personnalisés
JuriDocument = Dict[str, Any]


def fetch_juri_document(document_id: str) -> Optional[JuriDocument]:
    """
    Récupère un document jurisprudentiel depuis l'API Legifrance.
    
    Args:
        document_id (str): Identifiant technique du document JURI à récupérer
    
    Returns:
        Optional[JuriDocument]: Document JURI au format JSON, ou None en cas d'échec
    
    Raises:
        ConnectionError: En cas d'échec de connexion à l'API
    """
    time.sleep(0.2)  # Pause pour éviter de surcharger l'API : pas d'erreur 429
    # Récupération du token d'authentification
    token = obtain_legifrance_token()
    
    if not token:
        print("Échec d'authentification: impossible d'obtenir un token Legifrance")
        return None
    
    # Configuration de la requête
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {"textId": document_id}
    
    # Envoi de la requête
    try:
        response = requests.post(
            f"{LEGIFRANCE_BASE_URL}/consult/juri",
            json=payload,
            headers=headers,
        )
        
        # Vérification de la réponse
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur HTTP {response.status_code}: {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"Erreur de connexion: {e}")
        return None


def extract_document_text(document: Optional[JuriDocument]) -> str:
    """
    Extrait le contenu textuel d'un document JURI.
    
    Args:
        document (Optional[JuriDocument]): Le document JURI
    
    Returns:
        str: Le texte du document, ou un message d'erreur si le document est invalide
    """
    if not document:
        return "Aucun document trouvé ou erreur lors de la récupération."
    
    return document.get("text", {}).get("texte", "Texte introuvable")


def extract_court_name(document: Optional[JuriDocument]) -> str:
    """
    Extrait le nom de la juridiction ayant rendu la décision.
    
    Args:
        document (Optional[JuriDocument]): Le document JURI
    
    Returns:
        str: Le nom de la juridiction, ou un message d'erreur si le document est invalide
    """
    if not document:
        return "Aucun document trouvé ou erreur lors de la récupération."
    
    return document.get("text", {}).get("juridiction", "Juridiction introuvable")


def extract_document_title(document: Optional[JuriDocument]) -> str:
    """
    Extrait le titre ou l'intitulé du document JURI.
    
    Args:
        document (Optional[JuriDocument]): Le document JURI
    
    Returns:
        str: Le titre du document, ou un message d'erreur si le document est invalide
    """
    if not document:
        return "Aucun document trouvé ou erreur lors de la récupération."
    
    return document.get("text", {}).get("titre", "Titre introuvable")


def extract_document_status(document: Optional[JuriDocument]) -> str:
    """
    Extrait l'état (statut) du document JURI.
    
    Args:
        document (Optional[JuriDocument]): Le document JURI
    
    Returns:
        str: L'état du document, ou un message d'erreur si le document est invalide
    """
    if not document:
        return "Aucun document trouvé ou erreur lors de la récupération."
    
    state = document.get("text", {}).get("etat")
    
    # Gestion des valeurs nulles
    if state is None:
        return "Aucun état trouvé"
    
    return state


def extract_document_start_date(document: Optional[JuriDocument]) -> str:
    """
    Extrait la date de début du document JURI.
    
    Args:
        document (Optional[JuriDocument]): Le document JURI
    
    Returns:
        str: La date de début du document, ou un message si non disponible
    """
    if not document:
        return "Aucun document trouvé ou erreur lors de la récupération."
    
    date_debut = document.get("text", {}).get("dateDebut")
    
    if date_debut is None:
        return "Aucune date de début trouvée"
    
    # Si la date est au format timestamp (en millisecondes)
    if isinstance(date_debut, (int, float)) or (isinstance(date_debut, str) and date_debut.isdigit()):
        try:
            timestamp = int(date_debut) / 1000  # Conversion en secondes
            return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            pass
    
    # Si la date est au format ISO
    if isinstance(date_debut, str) and 'T' in date_debut:
        try:
            return date_debut.split('T')[0]  # Garder seulement la partie date
        except:
            pass
    
    return str(date_debut)


def extract_document_end_date(document: Optional[JuriDocument]) -> str:
    """
    Extrait la date de fin du document JURI.
    
    Args:
        document (Optional[JuriDocument]): Le document JURI
    
    Returns:
        str: La date de fin du document, ou un message si non disponible
    """
    if not document:
        return "Aucun document trouvé ou erreur lors de la récupération."
    
    date_fin = document.get("text", {}).get("dateFin")
    
    if date_fin is None:
        return "Aucune date de fin trouvée"
    
    # Si la date est au format timestamp (en millisecondes)
    if isinstance(date_fin, (int, float)) or (isinstance(date_fin, str) and date_fin.isdigit()):
        try:
            timestamp = int(date_fin) / 1000  # Conversion en secondes
            return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            pass
    
    # Si la date est au format ISO
    if isinstance(date_fin, str) and 'T' in date_fin:
        try:
            return date_fin.split('T')[0]  # Garder seulement la partie date
        except:
            pass
    
    return str(date_fin)


def get_juri_document_metadata(document_id: str) -> Dict[str, str]:
    """
    Récupère et extrait toutes les métadonnées d'un document JURI.
    
    Args:
        document_id (str): Identifiant technique du document JURI
    
    Returns:
        Dict[str, str]: Dictionnaire des métadonnées du document
    """
    document = fetch_juri_document(document_id)
    
    if not document:
        return {
            "error": "Document introuvable ou erreur lors de la récupération",
            "document_id": document_id
        }
    
    # Extraction des métadonnées
    metadata = {
        "document_id": document_id,
        "origine": "JURI",
        "titre": extract_document_title(document),
        "juridiction": extract_court_name(document),
        "etat": extract_document_status(document),
        "date_debut": extract_document_start_date(document),
        "date_fin": extract_document_end_date(document),
        "texte": extract_document_text(document)
    }
    
    return metadata


def print_juri_document(document_id: str) -> None:
    """
    Récupère et affiche de manière formatée les informations d'un document JURI.
    
    Args:
        document_id (str): Identifiant technique du document JURI
    
    Returns:
        None: La fonction affiche les informations sans retourner de valeur
    """
    metadata = get_juri_document_metadata(document_id)
    
    # Affichage formaté des informations
    if "error" in metadata:
        print(f"Erreur: {metadata['error']}")
        return
    
    print(f"> ID du document: {metadata['document_id']}")
    print(f"> Origine: {metadata['origine']}")
    print(f"> Titre: {metadata['titre']}")
    print(f"> Juridiction: {metadata['juridiction']}")
    print(f"> État: {metadata['etat']}")
    print(f"> Date de début: {metadata['date_debut']}")
    print(f"> Date de fin: {metadata['date_fin']}")
    print(f"> Texte: {metadata['texte']}...")  # Affichage du début du texte uniquement
    print("\n")


if __name__ == "__main__":
    
    # Exemple d'utilisation de la fonction principale
    example_id = "JURITEXT000051311766"  # Exemple d'ID de document JURI
    print_juri_document(example_id)