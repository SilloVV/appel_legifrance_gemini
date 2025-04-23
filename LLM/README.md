"""
Cette section du code est dédiée à l'intégration des modèles de langage tels que Gemini et Mistral. 
Elle permet de configurer et d'utiliser ces modèles pour des tâches spécifiques, en assurant une 
interopérabilité et une gestion efficace des ressources associées. Les modèles intégrés peuvent être 
utilisés pour des applications variées, notamment le traitement du langage naturel, la génération de 
texte, et d'autres cas d'utilisation liés à l'intelligence artificielle.
"""
## Architecture :
├── SEARCH/                       # Fonctionnalités de recherche
│   ├── search_call.py            # Appel à l'API de recherche
│   └── payload_explication.txt   # Documentation des payloads
├── LLM/                          # Intégration des modèles de langage
│   ├── __init__.py
│   ├── env_variable_loader.py    # Chargeur de variables d'environnement
│   ├── init_gemini.py            # Initialisation du modèle Gemini
│   └── init_mistral.py           # Initialisation du modèle Mistral