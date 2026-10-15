from dlt.common.schema.typing import TWriteDisposition
from dlt.sources.rest_api.typing import Endpoint, EndpointResource, PaginatorConfig


def api_endpoint(path: str, paginator: PaginatorConfig, data_selector: str) -> Endpoint:

    return {
        "path": path,
        "paginator": paginator,
        "data_selector": data_selector,
    }


def api_resource(
    name: str,
    pk: list[str],
    columns: dict,
    processing_steps: list,
    endpoint: Endpoint,
    write_disposition: TWriteDisposition = "replace",
) -> EndpointResource:
    if pk not in columns:
        raise ValueError(f"{pk} should be in columns")
    return {
        "name": name,
        "write_disposition": write_disposition,
        "primary_key": pk,
        "columns": columns,
        "processing_steps": processing_steps,
        "endpoint": endpoint,
    }
