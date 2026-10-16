import dlt

from pipelines.agriculture.source import ofb


def run(pipeline_name: str = "agriculture") -> None:
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination="filesystem",
        dataset_name="agriculture",
    )
    load_info = pipeline.run(ofb(), loader_file_format="parquet")
    load_info.raise_on_failed_jobs()
    print(load_info)


if __name__ == "__main__":
    run()
