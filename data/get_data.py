import requests

def get_data(taxon_id: int, size: int = 300):
    """
    :param taxon_id: Entier correspondant au taxonID OBIS (exemple : https://obis.org/taxon/137092)
    :param size: Nombre de résultats à renvoyer
    :return: Données JSON de l’API OBIS ou None en cas d’erreur
    """

    base_url = "https://api.obis.org/v3/occurrence"

    params = {
        "taxon_id": taxon_id,
        "size": size
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.RequestException as err:
        print(f"Erreur lors de la requête API OBIS : {err}")
        return None

    return response.json()