from pipelines.resources import api_endpoint, api_resource
from pipelines.sources import api_source


def ips_lycees():
    resource = api_resource(
        name="ips_lycees",
        pk=["uai", "rentree_scolaire"],
        columns={
            "uai": {"data_type": "text"},
            "rentree_scolaire": {"data_type": "text"},
            "ips_voie_gt": {"data_type": "double"},
            "ips_voie_pro": {"data_type": "double"},
            "ips_ensemble_gt_pro": {"data_type": "double"},
            "ecart_type_de_l_ips_voie_gt": {"data_type": "double"},
            "ecart_type_de_l_ips_voie_pro": {"data_type": "double"},
        },
        processing_steps=[],
        endpoint=api_endpoint(
            path="fr-en-ips_lycees/exports/json",
            paginator={"type": "single_page"},
            data_selector="$",
        ),
    )

    return api_source(
        base_url="https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/",
        source_name="ips_lycee",
        resources=[resource],
    )
