with ips as (
    select
        code_commune,
        any_value(nom_commune) as nom_commune,
        any_value(code_departement) as code_departement,
        count(*) as nb_lycees,
        count(*) filter (where secteur = 'public') as nb_lycees_publics,
        count(*) filter (where secteur = 'privé sous contrat')
            as nb_lycees_prives,
        round(avg(ips_ensemble_gt_pro), 1) as ips_moyen,
        min(ips_ensemble_gt_pro) as ips_min,
        max(ips_ensemble_gt_pro) as ips_max
    from {{ ref('int_education__ips_lycees_derniere_rentree') }}
    where code_commune is not null
    group by code_commune
)

select
    ips.code_commune,
    ips.nom_commune,
    ips.code_departement,
    ips.nb_lycees,
    ips.nb_lycees_publics,
    ips.nb_lycees_prives,
    ips.ips_moyen,
    ips.ips_min,
    ips.ips_max,
    tc.geom
from ips
inner join
    {{ ref('int_transverse__contour_communes') }} as tc
    on ips.code_commune = tc.code
where ips.code_commune is not null
