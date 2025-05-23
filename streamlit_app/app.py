import streamlit as st
import json
import time
import re
import sys
import os

# Déterminer le chemin absolu du répertoire racine du projet
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Ajouter le dossier racine au sys.path
sys.path.append(ROOT_DIR)

# Importer les modules du projet principal
from LEGIFRANCE_UTILS.payload.payload_generator import create_payload
from SEARCH.search_call import search_call
from LEGIFRANCE_UTILS.synthetize.synthetize_response import synthesize_legal_response

# Configuration de la page Streamlit
st.set_page_config(
    page_title="JERRY - Assistant de recherche juridique",
    page_icon="",
    layout="wide"
)

# Titre et description de l'application
st.title("🔍 JERRY - Assistant de recherche juridique")
st.markdown("""
Posez une question juridique pour obtenir une réponse basée sur les textes légaux et la jurisprudence française.
""")

# Fonction pour extraire les sources du texte de la réponse
def extract_sources(text):
    # Chercher la section des sources
    sources_section = re.search(r'## SOURCES:(.*?)(?=##|$)', text, re.DOTALL)
    if sources_section:
        sources_text = sources_section.group(1).strip()
        # Supprimer les mentions de documents insuffisants
        sources_text = re.sub(r'# Documents insuffisants', '', sources_text)
        sources_text = re.sub(r'#documents insuffisants', '', sources_text)
        # Vérifier si les documents étaient insuffisants
        insufficient = "Connaissances juridiques générales" in text
        return sources_text, insufficient
    return "", False

# Fonction pour extraire la réponse principale
def extract_response(text):
    response_section = re.search(r'## RÉPONSE :(.*?)(?=## SOURCES:|$)', text, re.DOTALL)
    if response_section:
        response_text = response_section.group(1).strip()
        # Ajouter un espace après "Éléments constitutifs :"
        response_text = re.sub(r'\*\*Éléments constitutifs :\*\*', '<strong>Éléments constitutifs :</strong>', response_text)
        return response_text
    return text

# Fonction pour formater les sources en liste
def format_sources_as_list(sources_text):
    """
    Transforme un texte contenant des sources en liste formatée Markdown
    """
    # Nettoyer le texte des sources
    sources_text = sources_text.replace("Connaissances juridiques générales", "")
    
    # Repérer les différentes sources (séparées par des astérisques)
    sources = sources_text.split('*')
    
    # Filtrer les entrées vides
    sources = [s.strip() for s in sources if s.strip()]
    
    # Formater chaque source comme un élément de liste avec des points (•)
    formatted_sources = ["• " + source for source in sources]
    
    return "\n".join(formatted_sources)

# Fonction principale pour traiter la question juridique
def process_juridical_question(user_question):
    with st.spinner("Génération du payload de recherche..."):
        # Générer le payload pour la recherche
        payload = create_payload(user_input=user_question)
        
    try:
        # Convertir la chaîne en objet JSON
        json_payload = json.loads(payload)
        
        with st.spinner("Recherche dans la base de données juridique..."):
            # Appel de l'API Legifrance
            api_results, error = search_call(json_payload)
            
            # Vérification de l'erreur
            if error:
                st.error(f"Erreur lors de la recherche: {error}")
                return
            
            if not api_results:
                st.warning("Aucun résultat juridique trouvé pour cette question.")
                return
        
        # Préparation des métadonnées pour la synthèse
        metadata_list = []
        
        with st.spinner("Analyse des documents juridiques..."):
            # Extraction des métadonnées à partir des résultats
            for result in api_results:
                # Utiliser le format standard (comme dans main.py)
                result_metadata = {
                    "title": result["titles"][0]["title"] if result.get("titles") else "Titre inconnu",
                    "id": result["titles"][0]["id"] if result.get("titles") else "",
                    "cid": result["titles"][0]["cid"] if result.get("titles") else "",
                    "type": result.get("type", ""),
                    "nature": result.get("nature", ""),
                    "origin": result.get("origin", ""),
                    "date": result.get("date", ""),
                    "extracts": []
                }
                
                # Ajout des extraits pertinents comme liste d'objets
                for section in result.get("sections", []):
                    for extract in section.get("extracts", []):
                        extract_data = {
                            "id": extract.get("id", ""),
                            "title": extract.get("title", "") or extract.get("num", "") or "Sans titre",
                            "section_title": section.get("title", ""),
                            "text": " ".join(extract.get("values", [])) if extract.get("values") else ""
                        }
                        result_metadata["extracts"].append(extract_data)
                
                metadata_list.append(result_metadata)
        
        with st.spinner("Génération de la réponse juridique..."):
            # Génération de la synthèse
            synthesis = synthesize_legal_response(user_question, metadata_list)
            return synthesis
            
    except json.JSONDecodeError:
        st.error("Une erreur est survenue lors de la préparation de la recherche.")
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
    
    return None

# Interface utilisateur principale
question = st.text_area("Votre question juridique:", height=100, 
                         placeholder="Exemple : Est-il possible de vendre des animaux vivants?")

# Bouton de soumission
if st.button("Rechercher", type="primary"):
    if not question:
        st.warning("Veuillez saisir une question.")
    else:
        # Stocker l'heure de début pour calculer le temps d'exécution
        start_time = time.time()
        
        # Traiter la question
        response = process_juridical_question(question)
        
        # Calculer le temps d'exécution
        execution_time = time.time() - start_time
        
        if response:
            # Extraire la réponse et les sources
            main_response = extract_response(response)
            sources_text, insufficient_docs = extract_sources(response)
            
            # Afficher la réponse principale dans un cadre
            st.markdown("### Réponse:")
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; border-left: 5px solid #b0302c;">
                {main_response}
            </div>
            """, unsafe_allow_html=True)
            
            # N'afficher la section des sources que si elle n'est pas vide
            if sources_text.strip():
                st.markdown("### Sources:")
                
                # Extraire les sources individuelles
                sources = [src.strip() for src in sources_text.split('*') if src.strip()]
                
                # Afficher chaque source comme un élément séparé avec des points
                for source in sources:
                    if source and not "documents insuffisants" in source.lower():
                        st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; border-left: 5px solid #4361ee;">
                    • {source}
                </div>
                """, unsafe_allow_html=True)
            
            if insufficient_docs:
                st.warning("Note: Les documents trouvés ne fournissent pas d'information spécifique sur ce sujet.")
            
            # Afficher le temps d'exécution
            st.caption(f"⏱️ Temps d'exécution: {execution_time:.2f} secondes")
            
# Pied de page avec des informations sur l'application
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p><small>JERRY - Assistant de recherche juridique basé sur l'API Légifrance et les modèles LLM</small></p>
</div>
""", unsafe_allow_html=True)