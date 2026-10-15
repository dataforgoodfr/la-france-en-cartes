# dlt's ingestion pipelines
pipeline name:
    uv run --directory pipelines python -m {{name}}.{{name}}_pipeline

education_pipeline: (pipeline "education")
transverse_pipeline: (pipeline "transverse")

pipelines: (pipeline "education") (pipeline "transverse")

parquet_to_pmtiles fichier:
    gpio pmtiles create "{{fichier}}" "webapp/public/data/{{file_stem(fichier)}}.pmtiles" --max-zoom 9 --force
