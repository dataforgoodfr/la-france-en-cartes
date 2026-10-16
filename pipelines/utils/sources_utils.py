import unicodedata
from collections.abc import Iterator

import polars as pl
from dlt.common.typing import TDataItems


def _flatten_geometry(feature: dict) -> dict:
    return {**feature["properties"], "geometry": feature["geometry"]}


def _strip_accents(text: str) -> str:
    # dlt supprime les lettres accentuees des noms de table ("complémentaire" -> "compl_mentaire")
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def read_excel(content: bytes, header_row: int = 0) -> Iterator[tuple[str, TDataItems]]:
    sheets = pl.read_excel(content, sheet_id=0, read_options={"header_row": header_row})
    for sheet_name, df in sheets.items():
        yield _strip_accents(str(sheet_name)), df.to_arrow()
