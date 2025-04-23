"""
Module pour récupérer et traiter les articles juridiques depuis l'API Legifrance.

Ce module fournit des fonctions pour:
- Interroger l'API Legifrance et récupérer des articles par leur identifiant
- Extraire différentes métadonnées des articles (texte, numéro, nature, état, etc.)
- Récupérer le titre du texte contenant l'article
- Afficher les informations de manière structurée et lisible

Les articles sont les unités de base des textes juridiques (lois, décrets, codes, etc.)
disponibles dans la base de données Legifrance.
"""
import requests
from typing import Dict, List, Optional, Any, Union, Tuple
import datetime, json, time
# Pour récupérer le token d'authentification
from LEGIFRANCE_UTILS.legifrance_init import obtain_legifrance_token

# Configuration des URLs d'API
LEGIFRANCE_BASE_URL = "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app"
LEGIFRANCE_PROD_URL = "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app"

# Types personnalisés
Article = Dict[str, Any]


def fetch_article(article_id: str) -> Optional[Article]:
    """
    Récupère un article depuis l'API Legifrance.
    
    Args:
        article_id (str): Identifiant technique de l'article
    
    Returns:
        Optional[Article]: Article au format JSON, ou None en cas d'échec
    
    Raises:
        ConnectionError: En cas d'échec de connexion à l'API
    """

    time.sleep(0.05)
    
    token = obtain_legifrance_token()
    
    if not token:
        print("Échec d'authentification: impossible d'obtenir un token Legifrance")
        return None
    
    # Configuration de la requête
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {"id": article_id}
    
    # Envoi de la requête
    try:
        response = requests.post(
            f"{LEGIFRANCE_BASE_URL}/consult/getArticle",
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


def extract_article_text(article_data: Optional[Article]) -> str:
    """
    Extrait le contenu textuel d'un article.
    
    Args:
        article_data (Optional[Article]): Les données de l'article
    
    Returns:
        str: Le texte de l'article, ou un message d'erreur si les données sont invalides
    """
    if not article_data:
        return "Aucun article trouvé ou erreur lors de la récupération."
    
    return article_data.get("article", {}).get("texte", "Texte introuvable")


def extract_article_origin(article_data: Optional[Article]) -> str:
    """
    Extrait l'origine (fond juridique) d'un article.
    
    Args:
        article_data (Optional[Article]): Les données de l'article
    
    Returns:
        str: L'origine de l'article, ou un message d'erreur si les données sont invalides
    """
    if not article_data:
        return "Aucun article trouvé ou erreur lors de la récupération."
    
    return article_data.get("article", {}).get("origine", "Origine introuvable")


def extract_article_nature_and_number(article_data: Optional[Article]) -> Tuple[str, str]:
    """
    Extrait la nature et le numéro d'un article.
    
    Args:
        article_data (Optional[Article]): Les données de l'article
    
    Returns:
        Tuple[str, str]: Un tuple contenant (nature, numéro) de l'article
    """
    if not article_data:
        return ("Nature introuvable", "Numéro introuvable")
    
    article_info = article_data.get("article", {})
    nature = article_info.get("nature", "Nature introuvable")
    number = article_info.get("num", "Numéro introuvable")
    
    return (nature, number)


def extract_article_status(article_data: Optional[Article]) -> str:
    """
    Extrait l'état (statut) d'un article.
    
    Args:
        article_data (Optional[Article]): Les données de l'article
    
    Returns:
        str: L'état de l'article, ou un message d'erreur si les données sont invalides
    """
    if not article_data:
        return "Aucun article trouvé ou erreur lors de la récupération."
    
    return article_data.get("article", {}).get("etat", "État introuvable")


def extract_text_title(article_data: Optional[Article]) -> str:
    """
    Extrait le titre du texte associé à l'article.
    
    Args:
        article_data (Optional[Article]): Les données de l'article
    
    Returns:
        str: Le titre du texte, ou un message d'erreur si les données sont invalides
    """
    if not article_data:
        return "Aucun article trouvé ou erreur lors de la récupération."
    
    text_titles = article_data.get("article", {}).get("textTitles", [])
    
    if text_titles and isinstance(text_titles, list) and len(text_titles) > 0:
        return text_titles[0].get("titre", "Titre du texte introuvable")
    
    return "Titre du texte introuvable"


def get_article_metadata(article_id: str) -> Dict[str, str]:
    """
    Récupère et extrait toutes les métadonnées d'un article.
    
    Args:
        article_id (str): Identifiant technique de l'article
    
    Returns:
        Dict[str, str]: Dictionnaire des métadonnées de l'article
    """
    article_data = fetch_article(article_id)
    
    if not article_data:
        return {
            "error": "Article introuvable ou erreur lors de la récupération",
            "article_id": article_id
        }
    
    # Extraction des métadonnées
    nature, number = extract_article_nature_and_number(article_data)
    status = extract_article_status(article_data)
    
    # Formatage de l'état
    formatted_status = f"EN {status}" if status == "VIGUEUR" else status
    
    metadata = {
        "article_id": article_id,
        "text_title": extract_text_title(article_data),
        "nature": nature,
        "number": number,
        "texte": extract_article_text(article_data),
        "origine": extract_article_origin(article_data),
        "etat": formatted_status
    }
    
    return metadata


def print_article(article_id: str, short_text: bool = False) -> None:
    """
    Récupère et affiche les informations d'un article de manière formatée.
    
    Args:
        article_id (str): Identifiant technique de l'article
        short_text (bool): Si True, affiche seulement un extrait du texte (défaut: False)
    
    Returns:
        None: La fonction affiche les informations sans retourner de valeur
    """
    metadata = get_article_metadata(article_id)
    
    # Vérification des erreurs
    if "error" in metadata:
        print(f"Erreur: {metadata['error']}")
        return
    
    # Vérifier l'état de l'article
    etat = metadata.get('etat', '')
    est_abroge = "ABROGE" in etat.upper() if etat else False
    est_initiale = "INITIALE" in etat.upper() if etat else False
    status_indicator = "[ABROGÉ] " if est_abroge else ("[INITIALE] " if est_initiale else "")
    
    # Extraire les dates importantes depuis les données de l'article (si disponibles)
    article_data = fetch_article(article_id)
    date_debut = "Non disponible"
    date_fin = "Non disponible"
    
    if article_data and "article" in article_data:
        # Conversion timestamp en date lisible
        if "dateDebut" in article_data["article"]:
            try:
                timestamp = int(article_data["article"]["dateDebut"]) / 1000
                date_debut = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                date_debut = article_data["article"]["dateDebut"]
                
        if "dateFin" in article_data["article"]:
            try:
                timestamp = int(article_data["article"]["dateFin"]) / 1000
                date_fin = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                date_fin = article_data["article"]["dateFin"]
    
    # Affichage des informations de base
    print(f">{status_indicator}ID de l'article : {metadata['article_id']}")
    print(f">Titre du texte associé à l'article : {metadata['text_title']}")
    print(f">Article : {metadata['nature']} {metadata['number']}")
    
    # Gestion spécifique pour l'affichage des dates selon l'état
    if est_initiale and date_debut == date_fin:
        print(f">Date de publication : {date_debut}")
    else:
        print(f">Date de début : {date_debut}")
        if est_abroge:
            print(f">Date de fin : {date_fin}")
        else:
            print(f">Date de fin : {date_fin if date_fin != 'Non disponible' and date_fin != date_debut else 'En vigueur'}")
    
    
    # Préparation du texte (complet ou extrait)
    texte = metadata['texte']
    if short_text and len(texte) > 150:
        texte_display = texte[:150] + "..."
    else:
        texte_display = texte
            
    print(f"> Contenu de l'article :\n {texte_display}")
    print(f">Fond juridique : {metadata['origine']}")
    
    # Toujours afficher l'état de l'article
    print(f">État de l'article : {metadata['etat']}")
    
def get_article_text_only(article_id: str) -> Optional[str]:
    """
    Récupère uniquement le contenu textuel d'un article.
    
    Cette fonction est utile pour l'extraction du texte à des fins d'analyse 
    ou de traitement automatisé.
    
    Args:
        article_id (str): Identifiant technique de l'article
    
    Returns:
        Optional[str]: Le texte de l'article, ou None en cas d'erreur
    """
    article_data = fetch_article(article_id)
    
    if not article_data:
        return None
    
    text = extract_article_text(article_data)
    
    return text if text != "Texte introuvable" else None


if __name__ == "__main__":
    # Exemple d'utilisation
    example_id = "JORFARTI000024080446"  # Exemple d'ID d'un article
    
    # Option 1: Afficher toutes les informations de l'article
    print("===== INFORMATIONS COMPLÈTES DE L'ARTICLE =====")
    print_article(example_id)
    
    # Option 2: Afficher les informations avec un texte abrégé
    # print("\n\n===== INFORMATIONS DE L'ARTICLE (TEXTE ABRÉGÉ) =====")
    # print_article(example_id, short_text=True)
    
    # Option 3: Récupérer uniquement le texte (pour traitement)
    # text_only = get_article_text_only(example_id)
    # print("\n\n===== TEXTE UNIQUEMENT =====")
    # print(text_only)
    
    #response = fetch_article(example_id)
    #print("\n\n===== RÉPONSE BRUTE DE L'API =====")
    #print(json.dumps(response, indent=4, ensure_ascii=False))