import dlt
from dlt.sources import DltResource, DltSource
from dlt.sources.rest_api.typing import EndpointResource

from pipelines.resources import api_resources


def api_source(
    base_url: str, source_name: str, resources: list[EndpointResource]
) -> DltSource:
    return build_source(source_name, *api_resources(base_url, *resources))


def build_source(name: str, *resources: DltResource) -> DltSource:
    @dlt.source(name=name)
    def source():
        return list(resources)

    return source()
