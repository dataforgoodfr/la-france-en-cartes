import os
import sys
from pathlib import Path

import duckdb

# Usage : python duckdb_to_pg.py [chemin/vers/lfe4.duckdb]
# Postgres : PG_URI, sinon variables libpq (PGHOST, PGUSER, PGPASSWORD...).
# S3 (marts en parquet sur S3) : S3_ENDPOINT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY.

DUCKDB_FILE = sys.argv[1] if len(sys.argv) > 1 else "lfe4.duckdb"


def sql_str(value):
    return "'" + value.replace("'", "''") + "'"


def pg_schema(schema, table):
    if schema == "main_raw":
        return "raw"
    if table.startswith("stg_"):
        return "stg"
    if table.startswith("int_"):
        return "int"
    if table.startswith("mart_"):
        return "marts"
    return None


db = Path(DUCKDB_FILE).stem
con = duckdb.connect()
con.execute("INSTALL postgres; LOAD postgres; INSTALL spatial; LOAD spatial;")
con.execute(f'ATTACH {sql_str(DUCKDB_FILE)} AS "{db}" (READ_ONLY)')

if os.getenv("S3_ENDPOINT"):
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute(f"""
        CREATE SECRET (
            TYPE s3,
            KEY_ID {sql_str(os.environ["AWS_ACCESS_KEY_ID"])},
            SECRET {sql_str(os.environ["AWS_SECRET_ACCESS_KEY"])},
            ENDPOINT {sql_str(os.environ["S3_ENDPOINT"])},
            URL_STYLE 'path',
            USE_SSL {os.getenv("S3_USE_SSL", "true")}
        )
    """)

con.execute(f"ATTACH {sql_str(os.getenv('PG_URI', ''))} AS pg (TYPE postgres)")

tables = con.execute(
    """
    SELECT schema_name, table_name FROM duckdb_tables()
    WHERE database_name = $db
    UNION ALL
    SELECT schema_name, view_name FROM duckdb_views()
    WHERE database_name = $db AND NOT internal
""",
    {"db": db},
).fetchall()

for schema, table in tables:
    target = pg_schema(schema, table)
    if target is None:
        continue
    cols = con.execute(
        """
        SELECT column_name, data_type FROM duckdb_columns()
        WHERE database_name = ? AND schema_name = ? AND table_name = ?
        ORDER BY column_index
    """,
        [db, schema, table],
    ).fetchall()
    select = ", ".join(
        f'ST_AsWKB("{c}")::BLOB AS "{c}"'
        if t.upper().startswith("GEOMETRY")
        else f'"{c}"'
        for c, t in cols
    )
    print(f"{schema}.{table} -> {target}.{table}")
    tmp = f"{table}__new"
    con.execute(f'CREATE SCHEMA IF NOT EXISTS pg."{target}"')
    con.execute(f'DROP TABLE IF EXISTS pg."{target}"."{tmp}"')
    con.execute(
        f'CREATE TABLE pg."{target}"."{tmp}" AS '
        f'SELECT {select} FROM "{db}"."{schema}"."{table}"'
    )

    con.begin()
    con.execute(f'DROP TABLE IF EXISTS pg."{target}"."{table}"')
    con.execute(f'ALTER TABLE pg."{target}"."{tmp}" RENAME TO "{table}"')
    con.commit()
