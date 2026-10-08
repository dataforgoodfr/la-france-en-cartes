select
    uai,
    nom_de_l_etablissment as nom_etablissement,
    secteur,
    type_de_lycee,
    code_insee_de_la_commune as code_commune,
    nom_de_la_commune as nom_commune,
    code_du_departement as code_departement,
    rentree_scolaire,
    ips_voie_gt,
    ips_voie_pro,
    ips_ensemble_gt_pro
from {{ ref('stg_education__ips_lycees') }}
qualify row_number() over (
    partition by uai
    order by rentree_scolaire desc
) = 1
