import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Usage : python marts_to_pmtiles.py [chemin/vers/manifest.json]
# Convertit en pmtiles les marts dont le meta contient export: pmtiles.
# Parquet lu dans DBT_EXTERNAL_ROOT (comme dbt), pmtiles ecrits dans PMTILES_DEST (s3://... ou dossier local).
# S3 : S3_ENDPOINT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY. Outils : gpio, tippecanoe, aws.

MANIFEST = sys.argv[1] if len(sys.argv) > 1 else "target/manifest.json"
EXTERNAL_ROOT = os.environ["DBT_EXTERNAL_ROOT"].rstrip("/")
DEST = os.environ["PMTILES_DEST"].rstrip("/")
MAX_ZOOM = "9"


def endpoint_url():
    endpoint = os.environ["S3_ENDPOINT"]
    if "://" in endpoint:
        return endpoint
    scheme = "https" if os.getenv("S3_USE_SSL", "true") == "true" else "http"
    return f"{scheme}://{endpoint}"


def copy(src, dst):
    if src.startswith("s3://") or dst.startswith("s3://"):
        subprocess.run(
            ["aws", "s3", "cp", src, dst, "--endpoint-url", endpoint_url()], check=True
        )
    else:
        Path(dst).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)


def pmtiles_models(manifest):
    for node in manifest["nodes"].values():
        if node["resource_type"] != "model" or "marts" not in node["fqn"]:
            continue
        # dbt >= 1.10 range le meta dans config, les versions precedentes a la racine
        meta = {**node.get("meta", {}), **node["config"].get("meta", {})}
        if meta.get("export") == "pmtiles":
            yield node, meta


manifest = json.loads(Path(MANIFEST).read_text())
models = list(pmtiles_models(manifest))
if not models:
    print("Aucun mart avec export: pmtiles")

with tempfile.TemporaryDirectory() as tmp:
    for node, meta in models:
        model = node["name"]
        # Nom du fichier et du layer, surchargeable par meta.pmtiles_name
        name = meta.get("pmtiles_name", model)
        # Meme emplacement que la materialisation external de dbt-duckdb
        location = node["config"].get("location") or f"{EXTERNAL_ROOT}/{model}.parquet"
        parquet = f"{tmp}/{model}.parquet"
        pmtiles = f"{tmp}/{name}.pmtiles"
        print(f"{location} -> {DEST}/{name}.pmtiles")
        copy(location, parquet)
        subprocess.run(
            [
                "gpio",
                "pmtiles",
                "create",
                parquet,
                pmtiles,
                "--layer",
                name,
                "--max-zoom",
                MAX_ZOOM,
                "--force",
            ],
            check=True,
        )
        copy(pmtiles, f"{DEST}/{name}.pmtiles")
