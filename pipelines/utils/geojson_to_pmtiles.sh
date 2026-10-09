#!/bin/bash

file_path="$1"
filename=$(basename -- "$file_path")
filename="${filename%.*}"
gpio pmtiles create $file_path webapp/public/data/${filename%.*}.pmtiles --max-zoom 9 --force
