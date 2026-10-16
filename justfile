# dlt's ingestion pipelines
pipeline name:
    uv run --directory pipelines python -m {{name}}.{{name}}_pipeline

education_pipeline: (pipeline "education")
transverse_pipeline: (pipeline "transverse")
#immigration_pipeline: (pipeline "immigration")
sante_pipeline: (pipeline "sante")
agriculture_pipeline: (pipeline "agriculture")

# Lance tous les pipelines en parallele (logs entremeles : lancer un pipeline seul pour deboguer)
[parallel]
pipelines: (pipeline "education") (pipeline "transverse") (pipeline "sante") (pipeline "agriculture")

# dbt (ex. just dbt build -t dev_s3). Chemins absolus vers ./data pour le target dev.
dbt *args:
    mkdir -p "{{justfile_directory()}}/data/dev/warehouse"
    LFE4_DATA_DIR="{{justfile_directory()}}/data" uv run --directory dbt/lfe4 dbt {{args}}

# Ingestion dlt puis build dbt, avec le meme profil (ex. just run dev_s3)
run profile="dev":
    WORKSPACE__PROFILE={{profile}} just pipelines
    just dbt build -t {{profile}}

# Supprime les donnees locales (lake + warehouse) et l'etat dlt d'un profil. Ne touche pas au S3.
[confirm("Supprimer data/<profil> et pipelines/.dlt/state/<profil> ?")]
clean profile="dev":
    rm -rf "{{justfile_directory()}}/data/{{profile}}" "{{justfile_directory()}}/pipelines/.dlt/state/{{profile}}"

parquet_to_pmtiles fichier:
    gpio pmtiles create "{{fichier}}" "webapp/public/data/{{file_stem(fichier)}}.pmtiles" --max-zoom 9 --force
