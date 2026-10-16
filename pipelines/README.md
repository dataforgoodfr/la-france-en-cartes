# Pipelines

L'ingestion de données se fait via [dlt](https://dlthub.com/docs/intro).
Chaque domaine a son propre dossier (education, agriculture, ...).

dlt fonctionne avec un système de sources et de ressources.
Dans ce repo, les sources sont les instituts ou sites web où l'on trouve les données (INSEE, data.gouv, DREES, ...).
Une ressource est l'une des données disponibles sur ces sites, API, ...

Pour chaque domaine, on définit les sources et leurs ressources dans `source.py`.
`<domaine>_pipeline.py` permet d'exécuter l'ingestion d'un domaine donné.

## Exécuter les pipelines

Les pipelines peuvent être exécutées grâce à des recettes just :

```bash
just sante_pipeline           # un domaine
just pipelines                # tous, en parallèle
```

### Profils

La destination dépend du [profil dlt](https://dlthub.com/docs/general-usage/credentials/setup) actif. La config commune est dans `.dlt/config.toml`. Chaque profil la surcharge avec `.dlt/<profil>.config.toml` et `.dlt/<profil>.secrets.toml`.

| Profil | Destination | Prérequis |
|---|---|---|
| `dev` (défaut) | local : `./data/dev/lake` (racine du repo) | aucun |
| `dev_s3` | MinIO local : `s3://lfe4/lake` | `docker compose up -d` + `cp .dlt/dev_s3.secrets.toml.example .dlt/dev_s3.secrets.toml` |
| `prod` | S3 de prod : `s3://<bucket>/lake` | `.dlt/prod.secrets.toml` (voir `.dlt/prod.secrets.toml.example`) ou variables d'environnement |

```bash
WORKSPACE__PROFILE=dev_s3 just pipelines   # ponctuel
echo dev_s3 > pipelines/.dlt/profile-name  # persistant (la variable d'env reste prioritaire)
```

L'état des pipelines est isolé par profil dans `.dlt/state/<profil>`.

> [!WARNING]
> dlt mémorise le dossier local (`local_dir`) au premier run de chaque pipeline. si le dossier d'écriture change, supprimer `.dlt/state/<profil>`

## Contribuer

### Nouveau domaine

Si vous travaillez sur un nouveau domaine, pensez à créer le répertoire dédié. Ce répertoire devra contenir `source.py` et `<domaine>_pipeline.py`, et ajouter la recette dans le `justfile`.

### Ajouter une ressource

#### API

Une ressource est décrite grâce à `api_resource` et `api_endpoint` :

```python
def ips_lycees():
    return api_resource(
        # nom de la ressource
        name="ips_lycees",
        # clé(s) primaire(s)
        pk=["uai", "rentree_scolaire"],
        # colonnes et typage, peut rester vide
        columns={
            "uai": {"data_type": "text"},
            "ips_voie_gt": {"data_type": "double"},
        },
        # adresse de l'endpoint où vit la donnée
        endpoint=api_endpoint(
            # éviter /records en général : préférer /exports/json
            path="fr-en-ips_lycees/exports/json",
            paginator={"type": "single_page"},
            data_selector="$",
        ),
    )
```

#### Fichier (xls, xlsx, csv, zip)

`file_resource` lit les fichiers qui matchent `file_glob` sous `bucket_url` et les passe à un reader :

```python
def bnvd_achats():
    return file_resource(
        bucket_url=OFB_BNVD,
        file_glob="BNVD_TRACABILITE_2024_ACHAT_2019-2023.zip",
        resource_name="bnvd_achats",
        reader=read_zip({".csv": partial(read_csv, separator=";"), ".xlsx": read_excel}),
    )
```

Le reader permet à dlt d'accéder à la donnée (voir [Readers existants](#readers-existants)).

### Brancher la ressource

`api_resources` regroupe les ressources d'une même API (même `base_url`) avant de les ajouter à une source grâce à `build_source` :

```python
EDUCATION_API = "url_qui_va_bien"


def education() -> DltSource:
    return build_source(
        "education",
        *api_resources(EDUCATION_API, ips_lycees()),
    )
```

`build_source` prend n'importe quelle `DltResource` : on peut mélanger API et fichiers.

## Readers existants

Dans `utils/sources_utils.py`. Un reader prend les bytes du fichier et yield les données.

| Reader | Usage | Suffixe |
|---|---|---|
| `read_excel(content, header_row=0)` | xls / xlsx, toutes les feuilles | nom de la feuille en snake_case |
| `read_csv(content, separator=";", encoding="utf-8")` | csv, tout en texte (`infer_schema_length=0`) | vide |
| `read_zip(readers)` | zip, dispatch par extension, récursif sur les zip imbriqués | nom du fichier en snake_case |

Paramétrer avec `partial` :

```python
reader=partial(read_excel, header_row=3)                     # header en 4e ligne
reader=partial(read_csv, separator=",", encoding="latin-1")
```

Pour ajouter un format, il faut écrire une fonction `(bytes) -> Iterator[tuple[str, TDataItems]]` dans `sources_utils.py`.
