parquet_to_pmtiles fichier:
    gpio pmtiles create "{{fichier}}" "webapp/public/data/{{file_stem(fichier)}}.pmtiles" --max-zoom 9 --force
