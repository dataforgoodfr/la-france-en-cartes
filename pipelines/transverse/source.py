import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


def _flatten_feature(feature: dict) -> dict:
    # code, nom, departement, region, epci + geometrie GeoJSON brute
    return {**feature["properties"], "geometry": feature["geometry"]}


@dlt.source(name="contour_communes_france_metropol")
def contour_communes():
    # Ressource data.gouv 12f8cdc9-5844-4666-a4b5-6385d5415f67 (Communes 2025 1000m, GeoJSON)
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://object.data.gouv.fr/contours-administratifs/2025/geojson/",
        },
        "resources": [
            {
                "name": "contour_communes",
                "write_disposition": "replace",
                "primary_key": ["code"],
                "columns": {
                    "code": {"data_type": "text"},
                    "geometry": {"data_type": "json"},
                },
                "processing_steps": [{"map": _flatten_feature}],
                "endpoint": {
                    "path": "communes-1000m.geojson",
                    "paginator": {"type": "single_page"},
                    "data_selector": "features",
                },
            },
        ],
    }

    yield from rest_api_resources(config)
