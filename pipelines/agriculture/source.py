from functools import partial

from dlt.sources import DltSource

from pipelines.resources import file_resource
from pipelines.sources import build_source
from pipelines.utils.sources_utils import read_csv, read_excel, read_zip

OFB_BNVD = "https://data.ofb.fr/catalogue/data-eaufrance/api/records/a69c8e76-13e1-4f87-9f9d-1705468b7221/attachments/"


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


def ofb() -> DltSource:
    return build_source("ofb", bnvd_achats())
