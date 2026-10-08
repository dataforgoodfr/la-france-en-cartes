import dlt
from pipelines.education.source import ips_lycees


def parquet_from_data_education_gouv(
    filepath="fr-en-ips_lycees/exports/parquet/", pipeline_name="ips_lycee"
):
    pipeline = dlt.pipeline(pipeline_name=pipeline_name, destination="filesystem")

    load_info = pipeline.run(ips_lycees(), loader_file_format="parquet")
    if hasattr(load_info, "raise_on_failed_jobs"):
        load_info.raise_on_failed_jobs()
    print(load_info)


if __name__ == "__main__":
    parquet_from_data_education_gouv()
