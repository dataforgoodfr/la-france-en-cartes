# La France en Cartes (lfe4)

WIP

## Exécuter dbt

Depuis la racine du repo :

```bash
just dbt build               # target dev
just dbt build -t dev_s3     # autre target
```

La recette crée `./data/dev/warehouse` si besoin.
En profil dev, les données sont écrites dans data/dev/warehouse

## Profils

Les targets dbt reprennent les [profils dlt](../../pipelines/README.md#profils) : chaque target lit le lake (`lake/`) écrit par le profil dlt du même nom et écrit ses sorties à côté, dans `warehouse/`.

| Target | Lake lu (`lake_root`) | Marts écrits (`external_root`) | Prérequis |
|---|---|---|---|
| `dev` (défaut) | `./data/dev/lake` | `./data/dev/warehouse` | pipelines lancées avec le profil dlt `dev` |
| `dev_s3` | `s3://lfe4/lake` (MinIO local) | `s3://lfe4/warehouse` | `docker compose up -d` |
| `prod` | `$DBT_LAKE_ROOT` | `$DBT_EXTERNAL_ROOT` | `DBT_LAKE_ROOT`, `DBT_EXTERNAL_ROOT`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_ENDPOINT` |

En `dev`, la base DuckDB est `./data/dev/warehouse/lfe4.duckdb`. Les marts y sont des vues sur les fichiers parquet. Pensez à charger l'extension `spatial` pour lire les colonnes géométriques.

```SQL
INSTALL spatial;
LOAD spatial;
```

Le target se choisit avec `-t` ou `DBT_TARGET`. `DBT_LAKE_ROOT` et `DBT_EXTERNAL_ROOT` surchargent aussi les valeurs par défaut de `dev` et `dev_s3`.
