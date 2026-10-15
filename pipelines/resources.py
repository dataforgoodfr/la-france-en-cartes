from dlt.common.schema.typing import TWriteDisposition
from dlt.sources.rest_api.typing import Endpoint, EndpointResource, PaginatorConfig


def api_endpoint(
    path: str,
    paginator: PaginatorConfig,
    data_selector: str,
    params: dict | None = None,
) -> Endpoint:
    endpoint: Endpoint = {
        "path": path,
        "paginator": paginator,
        "data_selector": data_selector,
    }
    if params:
        endpoint["params"] = params
    return endpoint


def api_resource(
    name: str,
    pk: list[str],
    columns: dict,
    processing_steps: list,
    endpoint: Endpoint,
    write_disposition: TWriteDisposition = "replace",
) -> EndpointResource:
    missing = [key for key in pk if key not in columns]
    if missing:
        raise ValueError(f"{missing} should be in columns")
    return {
        "name": name,
        "write_disposition": write_disposition,
        "primary_key": pk,
        "columns": columns,
        "processing_steps": processing_steps,
        "endpoint": endpoint,
    }
