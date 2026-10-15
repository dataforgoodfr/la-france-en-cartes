def _flatten_geometry(feature: dict) -> dict:
    return {**feature["properties"], "geometry": feature["geometry"]}
