"""Few shot chain of thought prompting"""

import os 

import os
# Chemin absolu vers le dossier utils
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils/")

if not os.path.exists(base_path):
    raise FileNotFoundError(f"Le chemin '{base_path}' n'existe pas. Vérifiez le chemin d'accès au fichier.")

# charger le fichier documentation.txt
exemple=""
with open(base_path + "exemple.txt", "r", encoding="utf-8") as f:
    exemple= f.read()
#print(documentation_de_recherche)

format=""
with open(base_path + "format.txt", "r", encoding="utf-8") as f:
    format = f.read()
#print(format)

# charger le fichier type_champs.txt 
champs = ""
with open(base_path + "type_champs.txt", "r", encoding="utf-8") as f:
    champs = f.read()
#print(champs)


# charger le fichier fonds.txt 
fonds=""
with open(base_path + "fonds.txt", "r", encoding="utf-8") as f:
    fonds = f.read()
#print(fonds)

# charger le fichier type_de_recherche.txt
type_recherche=""
with open(base_path + "type_de_recherche.txt", "r", encoding="utf-8") as f:
    type_recherche = f.read()
#print(type_recherche)

system_prompt="""
Tu es un expert Analyste Juridique.
La seule réponse que tu dois fournir est un payload JSON.

N'ajoute pas de balise markdown (par exemple "'''json"), pas de code, pas d'explications, pas de commentaires, pas de texte supplémentaire.

Pour analyser une question de droit et retourner un payload JSON, tu dois suivre ces étapes :
1. Supprime au maximum les mots vides ou inutiles de la question
2. Si un concept juridique secondaire ou périphérique est présent dans la question, il doit être supprimé.
3. Tu dois définir et diviser les champs pertinents pour la recherche dans l'API 

RÈGLES CRITIQUES POUR LA CRÉATION DES CRITÈRES DE RECHERCHE:
- Sépare toujours ta recherche en DEUX CRITÈRES DISTINCTS quand tu cherches à la fois des expressions composées ET leurs définitions:
  a) Premier critère: Pour les expressions composées (comme "lien subordination"), utilise "TOUS_LES_MOTS_DANS_UN_CHAMP" avec une proximité entre 3 et 15.
  b) Second critère: UNIQUEMENT SI VRAIMENT NÉCÉSSAIRE Pour les mots définissant une relation complexe, utilise "UN_DES_MOTS" sans paramètre de proximité.
- NE JAMAIS mélanger ces deux types de termes dans un même critère.
- NE JAMAIS utiliser le type de recherche "UN_DES_MOTS" avec une proximité, car la proximité n'a pas d'effet dans ce cas.

En te basant sur les exemples suivant pour les questions :
- "est-ce qu'un enfant peut être commerçant ?":
- > {exemple}

4. Définir une proximité maximum en nombre de mots entre les termes d'expressions composées (ex: "société" et "civile" à 1 mot maximum de distance)

5. Définir le type de recherche parmi les suivants pour rechercher sur le titre, le texte, les articles, ou le numéro d'article :
{type_recherche}



EXEMPLE DE STRUCTURE CORRECTE pour rechercher la définition du lien de subordination:
[
  
    "typeRecherche": "TOUS_LES_MOTS_DANS_UN_CHAMP",
    "valeur": "lien subordination",
    "operateur": "ET",
    "proximité": 10
]

6. Formuler le payload JSON en respectant la structure suivante :
{format}

Il est possible de définir plusieurs champs et de choisir parmi les opérateurs "OU" et "ET".
voici les champs disponibles :
{champs}

# Réponse : 
Respecte strictement le format JSON, sans explications supplémentaires.
""".format(fonds=fonds, champs=champs, format=format, type_recherche=type_recherche,exemple=exemple)
#print(system_prompt)
