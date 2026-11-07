from functools import partial

from dlt.sources import DltSource

from pipelines.resources import file_resource
from pipelines.sources import build_source
from pipelines.utils.sources_utils import read_csv, read_excel, read_zip

OFB_BNVD = "https://data.ofb.fr/catalogue/data-eaufrance/api/records/a69c8e76-13e1-4f87-9f9d-1705468b7221/attachments/"
INSEE_BASE_URL = "https://www.insee.fr/fr/statistiques/fichier"


def bnvd_achats():
    # Banque nationale des ventes de produits phytosanitaires (BNVD),
    # achats 2019-2023 par code postal, departement et France
    return file_resource(
        bucket_url=OFB_BNVD,
        file_glob="BNVD_TRACABILITE_2024_ACHAT_2019-2023.zip",
        resource_name="bnvd_achats",
        reader=read_zip(
            {".csv": partial(read_csv, separator=";"), ".xlsx": read_excel}
        ),
    )


def insee_exploitants_agricoles():
    return file_resource(
        bucket_url=f"{INSEE_BASE_URL}/7728869/",
        file_glob="AGRI24-F16.xlsx",
        resource_name="insee_exploitants_agricoles",
        reader=read_excel,
    )


def insee_nbr_exploitations():
    return file_resource(
        bucket_url=f"{INSEE_BASE_URL}/7728861/",
        file_glob="AGRI24-F12.xlsx",
        resource_name="insee_nbr_exploitations",
        reader=read_excel,
    )


def insee_main_oeuvre_agricole():
    return file_resource(
        bucket_url=f"{INSEE_BASE_URL}/7728865/",
        file_glob="AGRI24-F14.xlsx",
        resource_name="insee_main_oeuvre_agricole",
        reader=read_excel,
    )


def ofb() -> DltSource:
    return build_source(
        "ofb",
        bnvd_achats(),
        insee_exploitants_agricoles(),
        insee_nbr_exploitations(),
        insee_main_oeuvre_agricole(),
    )
