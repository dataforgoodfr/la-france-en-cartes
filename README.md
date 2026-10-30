# Template DataForGood

This file will become your README and also the index of your
documentation.

# Contributing


## Installation

- [Installation de Python](#installation-de-python)

Ce projet utilise [uv](https://docs.astral.sh/uv/) pour la gestion des dépendances Python. Il est préréquis pour l'installation de ce projet.

Une fois installé, il suffit de lancer la commande suivante pour installer la version de Python adéquate, créer un environnement virtuel et installer les dépendances du projet.

```bash
uv sync
```

A l'usage, si vous utilisez VSCode, l'environnement virtuel sera automatiquement activé lorsque vous ouvrirez le projet. Sinon, il suffit de l'activer manuellement avec la commande suivante :

```bash
source .venv/bin/activate
```

Ou alors, utilisez la commande `uv run ...` (au lieu de `python ...`) pour lancer un script Python. Par exemple:

```bash
uv run pipelines/run.py run build_database
```


## Lancer les precommit-hook localement

[Installer les precommit](https://pre-commit.com/)

    uv tool install pre-commit
    uv sync                      # installe ruff, sqlfluff et pyright aux versions de uv.lock
    pre-commit install

    pre-commit run --all-files


## Utiliser Tox pour tester votre code

    tox -vv

## Utiliser le serveur S3

Démarrer le serveur

```bash
docker-compose up -d
```

Vérifier l'état du serveur

```
docker exec garage /garage status
```

Stopper le serveur

```bash
docker-compose up -d
```

Voir les logs du serveur

```bash
docker logs garage
```

Attention. En cas d'erreur de permission, il y a deux solutions possibles :

1. créer un group `docker` et y ajouter son compte (recommandé)
   voir [Linux post-installation steps for Docker Engine | Docker Docs](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
2. utiliser `sudo`
