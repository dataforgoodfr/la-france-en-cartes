#!/bin/bash

file_path="$1"
duckdb -c "INSTALL spatial; LOAD spatial;
COPY (SELECT * FROM read_parquet('$file_path')) TO
'${file_path%.*}.geojson' WITH (FORMAT GDAL, DRIVER 'GeoJSON', LAYER_NAME 'ips_communes');"
