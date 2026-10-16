from functools import partial

from dlt.sources import DltSource

from pipelines.resources import api_endpoint, api_resource, api_resources, file_resource
from pipelines.sources import build_source
from pipelines.utils.sources_utils import read_excel


def professionnels_sante_1999_2011():
    # DREES : effectifs des professionnels de sante 1999-2011 (repertoire Adeli), .xls
    return file_resource(
        bucket_url="https://data.drees.solidarites-sante.gouv.fr/api/datasets/1.0/514_la-demographie-des-professionnels-de-sante-de-1999-a-2011/attachments/",
        file_glob="series_professionnels_de_sante_1999_2011_adeli_xls",
        # resource_name="drees_professionnels_sante_adeli",
        resource_name="adeli_1999_2011",
        reader=partial(read_excel, header_row=3),
    )


def medecins_2012_2026():
    # DREES : effectifs des professionnels de sante 2012-2026 (repertoire Adeli), .xls
    return file_resource(
        bucket_url="https://data.drees.solidarites-sante.gouv.fr/api/datasets/1.0/la-demographie-des-professionnels-de-sante-depuis-2012/attachments/",
        file_glob="medecins_rpps_2012_2026_xlsx/",
        resource_name="medecins_rpps_2012_2026",
        reader=read_excel,
    )


DREES_API = (
    "https://data.drees.solidarites-sante.gouv.fr/api/explore/v2.1/catalog/datasets/"
)


def apl_medico_social():
    # APL aux structures medico-sociales destinees aux personnes agees, par commune
    return api_resource(
        name="apl_medico_social",
        pk=["code_com"],
        processing_steps=[],
        columns={
            "code_com": {"data_type": "text"},
            "apl_ehpa": {"data_type": "double"},
            "apl_ra": {"data_type": "double"},
            "apl_sapa": {"data_type": "double"},
        },
        endpoint=api_endpoint(
            path="accessibilite-potentielle-localisee-apl-aux-structures-medico-sociales-destinees/exports/json",
            paginator={"type": "single_page"},
            data_selector="$",
        ),
    )


def drees() -> DltSource:
    return build_source(
        "drees",
        professionnels_sante_1999_2011(),
        medecins_2012_2026(),
        *api_resources(DREES_API, apl_medico_social()),
    )
