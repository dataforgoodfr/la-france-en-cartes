parquet_to_pmtiles fichier:
    gpio pmtiles create "{{fichier}}" "webapp/public/data/{{file_stem(fichier)}}.pmtiles" --max-zoom 9 --force

# Active le versioning du bucket du tfstate (Cellar) et affiche son statut
tfstate-versioning:
    #!/usr/bin/env bash
    set -euo pipefail
    set -a; source infra/.env; set +a
    endpoint=https://cellar-c2.services.clever-cloud.com
    bucket="${TF_VAR_state_bucket_name:-tfstate-bucket-d4g-lfe4}"
    aws s3api put-bucket-versioning --bucket "$bucket" --versioning-configuration Status=Enabled --endpoint-url "$endpoint"
    aws s3api get-bucket-versioning --bucket "$bucket" --endpoint-url "$endpoint"
