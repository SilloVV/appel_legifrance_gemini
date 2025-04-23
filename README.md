
# Projet d'Assistant Juridique - Légifrance API
## Pipeline de l'outil :
![Pipeline du projet](/image_readme/pipeline.png "Pipeline complète")

## Description

Ce projet est un assistant juridique qui utilise l'API Légifrance pour effectuer des recherches juridiques à partir de questions en langage naturel. Il génère des synthèses intelligentes en utilisant des modèles de langage avancés (LLM).

## Structure du projet

```
.
├── LEGIFRANCE_UTILS/              # Utilitaires pour l'API Légifrance
│   ├── legifrance_init.py         # Initialisation de la connexion à l'API
│   ├── display_article/           # Affichage des articles juridiques
│   │   └── get_article_from_id.py # Récupération d'articles par ID
│   ├── payload/                   # Gestion des payloads API
│   │   ├── parse_payload.py       # Traitement des payloads
│   │   ├── payload_generator.py   # Générateur de payloads
│   │   └── payload_prompt/        # Prompts pour la génération
│   │       ├── create_payload.py  # Création des prompts
│   │       └── utils/             # Fichiers utilitaires pour les prompts
│   └── synthetize/                # Synthèse des réponses juridiques
│       └── synthetize_response.py # Génération de synthèses
│
├── LLM/                          # Intégration des modèles de langage
│   ├── __init__.py
│   ├── env_variable_loader.py    # Chargeur de variables d'environnement
│   ├── init_gemini.py            # Initialisation du modèle Gemini
│   └── init_mistral.py           # Initialisation du modèle Mistral
│
├── SEARCH/                       # Fonctionnalités de recherche
│   ├── search_call.py            # Appel à l'API de recherche
│   └── payload_explication.txt   # Documentation des payloads
│
├── streamlit_app/                # Application Streamlit
│   ├── app.py                    # Application principale
│   ├── requirements.txt          # Dépendances spécifiques
│   ├── run.sh                    # Script de lancement
│   ├── .streamlit/              
│   │   └── config.toml           # Configuration Streamlit
│   └── resultats_legifrance.json # Exemple de résultats de recherche
│
├── main.py                       # Script principal
├── tool.py                       # Outil de recherche juridique
├── requirements.txt              # Dépendances du projet
├── .env_example                  # Exemple de fichier .env
└── .gitignore                    # Fichiers à ignorer par git
```

## Configuration requise

1. Python 3.8+
2. Clés API pour:
   - Légifrance (client ID et secret)
   - Modèles LLM (Gemini, Mistral)

## Installation

1. Cloner le dépôt
```bash
git clone <url-du-dépôt>
cd <nom-du-dépôt>
```

2. Installer les dépendances
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement
```bash
cp .env_example .env
# Éditer le fichier .env avec vos clés API
```

## Utilisation

### Ligne de commande

```bash
python main.py
# Suivez les instructions pour poser votre question juridique
```

### Comme module Python

```python
from tool import search_legifrance

# Poser une question juridique
question = "Est-ce qu'un enfant peut être commerçant ?"
result = search_legifrance(question)
print(result)
```

### Application Streamlit

```bash
cd streamlit_app
chmod +x run.sh
./run.sh
# Ouvrez votre navigateur à l'adresse indiquée
```

## Fonctionnalités principales

1. **Génération de payload**: Transforme une question en langage naturel en requête JSON structurée pour l'API Légifrance
2. **Recherche juridique**: Interroge la base de données Légifrance via son API
3. **Extraction d'articles**: Récupère et traite les articles juridiques pertinents
4. **Synthèse intelligente**: Génère une réponse claire et structurée basée sur les documents trouvés
5. **Interface utilisateur**: Application Streamlit pour une utilisation conviviale

## Structure des modules

### LEGIFRANCE_UTILS
Contient tous les utilitaires nécessaires pour interagir avec l'API Légifrance:
- Authentification et gestion des tokens
- Génération de requêtes (payloads)
- Récupération et affichage d'articles

### LLM
Gère l'intégration des modèles de langage (Gemini, Mistral):
- Initialisation des clients API
- Chargement des variables d'environnement
- Configuration des modèles

### SEARCH
Fournit les fonctionnalités de recherche dans la base Légifrance:
- Construction et envoi des requêtes
- Traitement et formatage des résultats

### Streamlit App
Application web pour une utilisation conviviale:
- Interface utilisateur intuitive
- Affichage formaté des résultats
- Configuration personnalisable

## Licences

Ce projet est sous licence [insérer licence]. Voir le fichier LICENSE pour plus de détails.

## Contributions

Les contributions sont les bienvenues! N'hésitez pas à signaler des bugs ou proposer des améliorations.