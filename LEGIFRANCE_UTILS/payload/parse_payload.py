
def parse_json_model_output(json_string:str)->str:
    """
    Nettoie la chaîne JSON pour la rendre valide
    """
    # enlever ce qu'il y a au dessus de '''json
    json_string = json_string.split("```json")[-1]
    
    # Remplace les guillemets simples par des guillemets doubles
    json_string = json_string.replace("```json", '')
    
    # enlever ce qu'il y a en dessous de ```
    json_string = json_string.split("```")[0]
    
    
    # Remplace les caractères de nouvelle ligne par des espaces
    json_string = json_string.replace("```", " ")
    
    
    return json_string
