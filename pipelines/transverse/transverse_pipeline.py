import dlt
from pipelines.transverse.source import contour_communes


def parquet_from_geo_gouv(pipeline_name="contour_communes"):
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination="filesystem",
        dataset_name="transverse",
    )

    load_info = pipeline.run(contour_communes(), loader_file_format="parquet")
    if hasattr(load_info, "raise_on_failed_jobs"):
        load_info.raise_on_failed_jobs()
    print(load_info)


if __name__ == "__main__":
    parquet_from_geo_gouv()
