select
    code,
    nom,
    departement,
    region,
    epci,
    ST_GEOMFROMGEOJSON(geometry) as geom
from {{ ref('stg_transverse__contour_communes') }}
