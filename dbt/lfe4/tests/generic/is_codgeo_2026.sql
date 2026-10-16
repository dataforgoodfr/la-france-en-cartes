{#
    Échoue si le codgeo n'est pas dans le ref 2026.
    Avec allow_hors_cog, les arrondissements et dom
    sont exclus.
#}

{% test is_codgeo_2026(model, column_name, allow_hors_cog=false) -%}
select distinct
    src.{{ column_name }}
from {{ model }} as src
where
    src.{{ column_name }} is not null
    and src.{{ column_name }} not in (
        select codgeo_2026 from {{ ref('codgeo_2003_2026') }}
    )
    {%- if allow_hors_cog %}
    and not regexp_full_match(
        src.{{ column_name }},
        '751(0[1-9]|1[0-9]|20)|6938[1-9]|132(0[1-9]|1[0-6])|97[578][0-9]{2}'
    )
    {%- endif %}
{%- endtest %}
