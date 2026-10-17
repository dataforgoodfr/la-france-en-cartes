{#
    Projette `relation` sur les codgeos 2026.

    Pour l'instant les fusions et scissions ne sont pas gérés.
    En particulier, pour les scissions, il faut utiliser la population
    En l'état, si le codegeo est absent du seed, on conserve tel quel

    Usage : {{ project_codgeo_2026(ref('mon_modele'), 'code_commune', 'nom') }}
#}

{% macro project_codgeo_2026(relation, codgeo_column, libgeo_column=none) -%}
with passage_codgeo_2026 as (
    select
        codgeo_ini,
        codgeo_2026,
        libgeo_2026
    from {{ ref('codgeo_2003_2026') }}
    qualify row_number() over (
        partition by codgeo_ini
        order by (codgeo_2026 = codgeo_ini) desc, codgeo_2026
    ) = 1
)

select
    src.* replace (
        coalesce(
            passage_codgeo_2026.codgeo_2026, src.{{ codgeo_column }}
        ) as {{ codgeo_column }}
    {%- if libgeo_column %},
        coalesce(
            passage_codgeo_2026.libgeo_2026, src.{{ libgeo_column }}
        ) as {{ libgeo_column }}
    {%- endif %}
    )
from {{ relation }} as src
left join passage_codgeo_2026
    on src.{{ codgeo_column }} = passage_codgeo_2026.codgeo_ini
{%- endmacro %}
