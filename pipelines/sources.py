from dlt.sources.rest_api import rest_api_source
from dlt.sources.rest_api.typing import EndpointResource, RESTAPIConfig


def api_source(base_url: str, source_name: str, resources: list[EndpointResource]):
    config: RESTAPIConfig = {
        "client": {"base_url": base_url},
        "resources": [*resources],
    }
    return rest_api_source(config, name=source_name)
