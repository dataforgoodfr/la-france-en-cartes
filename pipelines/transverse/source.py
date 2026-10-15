from pipelines.resources import api_endpoint, api_resource
from pipelines.sources import api_source
from pipelines.utils.sources_utils import _flatten_geometry


def contour_communes():
    # Ressource data.gouv 12f8cdc9-5844-4666-a4b5-6385d5415f67 (Communes 2025 1000m, GeoJSON)
    resource = api_resource(
        name="contour_communes",
        pk=["code"],
        columns={
            "code": {"data_type": "text"},
            "geometry": {"data_type": "json"},
        },
        processing_steps=[{"map": _flatten_geometry}],
        endpoint=api_endpoint(
            path="communes-1000m.geojson",
            paginator={"type": "single_page"},
            data_selector="features",
        ),
    )

    return api_source(
        base_url="https://object.data.gouv.fr/contours-administratifs/2025/geojson/",
        source_name="contour_communes_france_metropol",
        resources=[resource],
    )
