select
    code,
    nom,
    departement,
    region,
    epci,
    geometry
from {{ source('transverse', 'contour_communes') }}
