```markdown
## Appel à l'endpoint /search de Legifrance

Cette section décrit l'appel à l'endpoint `/search` de Legifrance. Le payload nécessaire pour cet appel a déjà été généré dans les étapes précédentes. Assurez-vous que les données du payload respectent les spécifications de l'API Legifrance pour garantir une réponse correcte.

### Étapes principales :
2. Effectuer l'appel HTTP vers l'endpoint `/search` avec e payload déja généré par le LEGIFRANCE_UTILS/payload/payload_generator.py
3. Traiter la réponse reçue.

├── SEARCH/                       # Fonctionnalités de recherche
│   ├── search_call.py            # Appel à l'API de recherche
│   └── payload_explication.txt   # Documentation des payloads