{#
    test idempotence
    codegeo 2026 vers codegeo 2026
#}

with codes_2026 as (
    select distinct
        codgeo_2026 as code_commune,
        libgeo_2026 as nom_commune,
        codgeo_2026 as code_origine,
        libgeo_2026 as nom_origine
    from {{ ref('codgeo_2003_2026') }}
),

projection_2026 as (
    {{ project_codgeo_2026('codes_2026', 'code_commune', 'nom_commune') }}
)

select
    code_origine,
    code_commune,
    nom_origine,
    nom_commune
from projection_2026
where code_commune != code_origine or nom_commune != nom_origine
