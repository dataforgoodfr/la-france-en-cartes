# Backend du tfstate

Ce dossier crée le stockage du tfstate d'`infra/` : un add-on Cellar (S3 Clever Cloud) et son bucket.

> ⚠️ **La création est à faire une seule fois pour tout le projet.** Si le bucket existe déjà, il suffit de configurer `infra/.env` et de vous connecter à Clever Cloud.

## Prérequis

- Un compte Clever Cloud membre de l'organisation du projet
- OpenTofu ≥ 1.8 et Clever Tools installés

## Se connecter à Clever Cloud

Exécutez `clever login`. Une page s'ouvre dans le navigateur et donne le token et secrets. Opentofu lit directement les creds importés par `clever login`.

Si open tofu ne trouve pas les creds, exportez les en var d'environnement :

    export CC_OAUTH_TOKEN=votre_token
    export CC_OAUTH_SECRET=votre_secret

Le token expire après un nouveau `clever login`.

## Configurer `infra/.env`

Toute la configuration passe par `infra/.env` (gitignoré, ne pas commit) :

    cp infra/.env.example infra/.env

- `TF_VAR_clever_organisation` : l'id de l'organisation (`orga_…`), visible dans la console Clever Cloud.
- `TF_VAR_state_passphrase` : la phrase de passe qui chiffre le state.
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` : les clés Cellar.
- `TF_VAR_state_bucket_name`, `TF_VAR_cellar_name` : facultatifs, pour changer les valeurs par défaut.

Avant de lancer `tofu`, chargez le fichier dans votre shell :

    set -a; source infra/.env; set +a
    # + les deux exports CC_OAUTH_* de « Se connecter à Clever Cloud »


## Créer le backend (bootstrap, une seule fois)

Le backend S3 ne peut pas être utilisé avant que le bucket existe. Depuis `infra/backend/`, avec `TF_VAR_clever_organisation` et `TF_VAR_state_passphrase` chargés (les clés Cellar n'existent pas encore) :

    mv backend.tf backend.tf.off   # state local le temps du bootstrap
    tofu init
    tofu plan                      # seuls l'add-on Cellar et son bucket doivent apparaître
    tofu apply
    mv backend.tf.off backend.tf
    # renseignez les clés Cellar dans infra/.env (voir plus bas), rechargez-le, puis :
    tofu init -migrate-state       # copie le state local dans le bucket
    tofu apply                     # « No changes » ; réécrit le state chiffré
    rm terraform.tfstate terraform.tfstate.backup


## Chiffrement du state

`encryption.tf` chiffre le state et les plans (AES-GCM, clé dérivée de `TF_VAR_state_passphrase` par PBKDF2).

**Changer de phrase de passe** : déclarez un second `key_provider "pbkdf2" "old"` avec l'ancienne phrase et un `method "aes_gcm" "old"`, mettez `fallback { method = method.aes_gcm.old }` dans `state`, lancez `tofu apply`, puis retirez l'ancienne méthode.

## Pas de verrou, mais des versions

> ⚠️ **Un seul `tofu apply` à la fois par dossier.** Le state n'est pas verrouillé. Deux `apply` simultanés peuvent s'écraser mutuellement le state.

Pour activer le versioning, depuis la racine du dépôt (la recette charge `infra/.env` elle-même) :

    just tfstate-versioning   # doit afficher "Status": "Enabled"

Le bucket visé est `TF_VAR_state_bucket_name` s'il est défini dans `infra/.env`, sinon `tfstate-bucket-d4g-lfe4`.

## Récupérer les creds Cellar

Deux options :
- **Console Clever Cloud** : add-on Cellar -> onglet de configuration (key ID / key secret).
- **Depuis le state** (une fois `tofu init` fait, ou en local pendant le bootstrap) : `tofu output -json cellar_creds`

Reportez-les dans `AWS_ACCESS_KEY_ID` et `AWS_SECRET_ACCESS_KEY` de `infra/.env`.
