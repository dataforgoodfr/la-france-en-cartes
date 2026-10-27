from dlt.sources import DltSource

from pipelines.resources import api_endpoint, api_resource, api_resources
from pipelines.sources import build_source

DATA_GOUV_API = "https://tabular-api.data.gouv.fr"


def chiffres_delinquance():
    return api_resource(
        # nom de la ressource
        name="chiffres_delinquance",
        # clé(s) primaire(s)
        pk=["Code_departement", "annee", "indicateur"],
        processing_steps=[],
        # colonnes et typage, peut rester vide
        columns={
            "unite_de_compte": {"data_type": "text"},
            "nombre": {"data_type": "bigint"},
            "taux_pour_mille": {"data_type": "double"},
        },
        # adresse de l'endpoint où vit la donnée
        endpoint=api_endpoint(
            # éviter /records en général : préférer /exports/json
            path="/api/resources/2b27a675-e3bf-41ef-a852-5fb9ab483967/data/json/",
            params={"page_size": 10},
            paginator={"type": "single_page"},
            data_selector="$",
        ),
    )


def securite() -> DltSource:
    return build_source(
        "securite",
        *api_resources(DATA_GOUV_API, chiffres_delinquance()),
    )
