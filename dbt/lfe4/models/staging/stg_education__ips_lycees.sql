select
    uai,
    nom_de_l_etablissment,
    secteur,
    type_de_lycee,
    code_insee_de_la_commune,
    nom_de_la_commune,
    code_du_departement,
    rentree_scolaire,
    ips_voie_gt,
    ips_voie_pro,
    ips_ensemble_gt_pro
from {{ source('education', 'ips_lycees') }}
