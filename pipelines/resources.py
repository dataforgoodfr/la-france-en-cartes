from collections.abc import Iterator

import dlt
from dlt.common.schema.typing import TColumnSchema, TWriteDisposition
from dlt.common.storages.fsspec_filesystem import FileItemDict
from dlt.sources import DltResource
from dlt.sources.filesystem import filesystem
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import (
    Endpoint,
    EndpointResource,
    PaginatorConfig,
    ProcessingSteps,
    RESTAPIConfig,
)

from pipelines.utils.sources_utils import FileReader


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
    endpoint: Endpoint,
    processing_steps: list[ProcessingSteps],
    columns: dict[str, TColumnSchema] | None = None,
    write_disposition: TWriteDisposition = "replace",
) -> EndpointResource:

    return {
        "name": name,
        "write_disposition": write_disposition,
        "primary_key": pk,
        "columns": columns,
        "processing_steps": processing_steps,
        "endpoint": endpoint,
    }


def api_resources(base_url: str, *resources: EndpointResource) -> list[DltResource]:
    config: RESTAPIConfig = {
        "client": {"base_url": base_url},
        "resources": [*resources],
    }
    return rest_api_resources(config)


def file_resource(
    bucket_url: str, file_glob: str, resource_name: str, reader: FileReader
):
    @dlt.transformer(name=resource_name, write_disposition="replace")
    def read_files(items: Iterator[FileItemDict]):
        for item in items:
            for table_suffix, rows in reader(item.read_bytes()):
                yield dlt.mark.with_table_name(rows, f"{resource_name}_{table_suffix}")

    return filesystem(bucket_url=bucket_url, file_glob=file_glob) | read_files
