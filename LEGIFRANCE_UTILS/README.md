## Architecture :
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

Cette partie contient les utilitaires pour l'api légifrance comme indiqué ce dessus.