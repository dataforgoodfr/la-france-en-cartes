# dlt's ingestion pipelines
pipeline name:
    uv run --directory pipelines python -m {{name}}.{{name}}_pipeline

education_pipeline: (pipeline "education")
transverse_pipeline: (pipeline "transverse")
immigration_pipeline: (pipeline "immigration")
sante_pipeline: (pipeline "sante")
agriculture_pipeline: (pipeline "agriculture")

# Lance tous les pipelines en parallele (logs entremeles : lancer un pipeline seul pour deboguer)
[parallel]
pipelines: (pipeline "education") (pipeline "transverse") (pipeline "immigration") (pipeline "sante") (pipeline "agriculture")

parquet_to_pmtiles fichier:
    gpio pmtiles create "{{fichier}}" "webapp/public/data/{{file_stem(fichier)}}.pmtiles" --max-zoom 9 --force
