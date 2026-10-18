# La France en Cartes

Les transformations/agrégations/join sont fait dans des modèles dbt.
dbt permet de gérer la data comme du code:
 - tests
 - macros (DRY)


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
| `pre_prod` | `$DBT_LAKE_ROOT` | `$DBT_EXTERNAL_ROOT` | `DBT_LAKE_ROOT`, `DBT_EXTERNAL_ROOT`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_ENDPOINT` |

En `dev`, la base DuckDB est `./data/dev/warehouse/lfe4.duckdb`. Les marts y sont des vues sur les fichiers parquet. Pensez à charger l'extension `spatial` pour lire les colonnes géométriques.

```SQL
INSTALL spatial;
LOAD spatial;
```

Le target se choisit avec `-t` ou `DBT_TARGET`. `DBT_LAKE_ROOT` et `DBT_EXTERNAL_ROOT` surchargent aussi les valeurs par défaut de `dev` et `dev_s3`.

## Contribuer


### Source

Afin de contribuer, la première étape est d'ajouter une source dans models/sources.
Les sources permettent d'alimenter les models staging à partir des parquets créés par dlt.
Dans la logique ELT, on charge les sources tel-quel, brutes.

### staging

Les models staging prennent leur source dans `sources`.
Ces models n'appliquent que des changements légés sur la donnée:
 - renommage
 - typing
 - conversion (centimes en euros par ex)
 - catégories (bucket, booléens)

A ce niveau, pas de joins ou d'agrégations.
Les models staging sont des views.

Les models sont organisés en sous-dossier par source (INSEE, data.gouv,...).

Conventions de noms:
    `stg_<source>__<entity>.sql`


### intermediate

Les models int sont organisés par sous-dossier thématique (immigration, santé,...)
Conventions de noms:
    `int_<theme>__<entity>.sql`

Ces models n'ont pas vocations à servir le front.
Dans cette couche, on fait les premières jointures. On change au besoin la granularité (communes->departements)
Les transformations complexes ont leur propre model afin d'assurer la lisibilité et maintenabilité.

Ces models sont des views.

### marts

Les marts sont dans la couche qui sert le front. Les données doivent être dénormalisées, prêtes à être utilisées.
Ils sont dans des sous-dossiers, par thèmes.

Conventions de noms:
    `mart_<theme>__<indicateur>.sql`

Cette couche est exportée en parquet.

## Best practices
Autant que faire ce peut, le code réutilisable doit être écrit en macro.
Les models doivent être testé.

## INSEE
Les données de l'INSEE peuvent avoir quelques subtilités:
 - codegeo millésimé sur une ancienne année (chaque année des communes sont fusionnées)
 - Arrondissement pour Paris, Lyon, Marseille - parfois seules les communes sont présentes, parfois seuls les arrondissements, parfois les deux
