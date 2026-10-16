import dlt

from pipelines.sante.source import drees


def parquet_from_drees(pipeline_name="drees_professionnels_sante_adeli"):
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination="filesystem",
        dataset_name="sante",
    )

    load_info = pipeline.run(drees(), loader_file_format="parquet")
    if hasattr(load_info, "raise_on_failed_jobs"):
        load_info.raise_on_failed_jobs()
    print(load_info)


if __name__ == "__main__":
    parquet_from_drees()
