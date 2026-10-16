import dlt
from dlt.sources import DltSource


def run_pipeline(domain: str, *sources: DltSource) -> None:
    pipeline = dlt.pipeline(
        pipeline_name=domain, destination="filesystem", dataset_name=domain
    )
    for source in sources:
        load_info = pipeline.run(source, loader_file_format="parquet")
        load_info.raise_on_failed_jobs()
        print(load_info)
