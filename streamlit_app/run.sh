#!/bin/bash

# Se placer dans le répertoire du script
cd "$(dirname "$0")"

# Vérifier que les dépendances sont installées
echo "Vérification et installation des dépendances..."
pip install -r requirements.txt

# Créer le dossier de configuration si nécessaire
mkdir -p .streamlit

# Lancer l'application Streamlit
echo "Démarrage de l'application JURI..."
streamlit run app.py