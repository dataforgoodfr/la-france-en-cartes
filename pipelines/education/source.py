import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source(name="ips_lycee")
def ips_lycees():
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/",
        },
        "resources": [
            {
                "name": "ips_lycees",
                "write_disposition": "replace",
                "primary_key": ["uai", "rentree_scolaire"],
                "columns": {
                    "ips_voie_gt": {"data_type": "double"},
                    "ips_voie_pro": {"data_type": "double"},
                    "ips_ensemble_gt_pro": {"data_type": "double"},
                    "ecart_type_de_l_ips_voie_gt": {"data_type": "double"},
                    "ecart_type_de_l_ips_voie_pro": {"data_type": "double"},
                },
                "endpoint": {
                    "path": "fr-en-ips_lycees/exports/json",
                    "paginator": {"type": "single_page"},
                    "data_selector": "$",
                },
            },
        ],
    }

    yield from rest_api_resources(config)
