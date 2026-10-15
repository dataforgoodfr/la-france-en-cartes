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


def evaluations_6eme_departement():
    resource = api_resource(
        name="evaluations_nationales_6eme_departement",
        # code_departement est vide pour les lignes "NATIONAL"
        pk=["annee", "libelle_departement", "discipline", "caracteristique"],
        columns={
            "annee": {"data_type": "text"},
            "libelle_departement": {"data_type": "text"},
            "code_departement": {"data_type": "text"},
            "discipline": {"data_type": "text"},
            "caracteristique": {"data_type": "text"},
            "ips_moyen": {"data_type": "double"},
            "score_moyen": {"data_type": "bigint"},
            "ecart_type": {"data_type": "double"},
        },
        processing_steps=[],
        endpoint=api_endpoint(
            path="fr-en-evaluations_nationales_6eme_departement/records",
            paginator={
                "type": "offset",
                "limit": 100,
                "offset_param": "offset",
                "limit_param": "limit",
                "total_path": "total_count",
            },
            data_selector="results",
            params={
                "order_by": "annee, libelle_departement, discipline, caracteristique"
            },
        ),
    )

    return api_source(
        base_url="https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/",
        source_name="evaluations_6eme",
        resources=[resource],
    )
