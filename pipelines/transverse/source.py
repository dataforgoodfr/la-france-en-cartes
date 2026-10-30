from dlt.sources import DltSource

from pipelines.resources import api_endpoint, api_resource, api_resources
from pipelines.sources import build_source
from pipelines.utils.sources_utils import _flatten_geometry

CONTOURS_ADMINISTRATIFS = (
    "https://object.data.gouv.fr/contours-administratifs/2025/geojson/"
)


def contour_communes():
    # Ressource data.gouv 12f8cdc9-5844-4666-a4b5-6385d5415f67 (Communes 2025 1000m, GeoJSON)
    return api_resource(
        name="contour_communes",
        pk=["code"],
        processing_steps=[{"map": _flatten_geometry}],
        columns={
            "code": {"data_type": "text"},
            "geometry": {"data_type": "json"},
        },
        endpoint=api_endpoint(
            path="communes-1000m.geojson",
            paginator={"type": "single_page"},
            data_selector="features",
        ),
    )


def transverse() -> DltSource:
    return build_source(
        "transverse",
        *api_resources(CONTOURS_ADMINISTRATIFS, contour_communes()),
    )
