import dlt

from pipelines.education.source import education


def run(pipeline_name: str = "education") -> None:
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination="filesystem",
        dataset_name="education",
    )
    load_info = pipeline.run(education(), loader_file_format="parquet")
    load_info.raise_on_failed_jobs()
    print(load_info)


if __name__ == "__main__":
    run()
