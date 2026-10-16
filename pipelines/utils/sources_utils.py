import io
import re
import unicodedata
import zipfile
from collections.abc import Callable, Iterator
from pathlib import Path

import polars as pl
from dlt.common.typing import TDataItems

# Reads the raw content of a file and yields (table_suffix, rows or dataframe) pairs
FileReader = Callable[[bytes], Iterator[tuple[str, TDataItems]]]


def _flatten_geometry(feature: dict) -> dict:
    return {**feature["properties"], "geometry": feature["geometry"]}


def _to_snake(name: str) -> str:
    """'Données 2025 (brut)' -> 'donnees_2025_brut'"""
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", ascii_name.lower()).strip("_")


def read_excel(content: bytes, header_row: int = 0) -> Iterator[tuple[str, TDataItems]]:
    sheets = pl.read_excel(content, sheet_id=0, read_options={"header_row": header_row})
    for sheet_name, df in sheets.items():
        yield _to_snake(str(sheet_name)), df.to_arrow()


def read_zip(readers: dict[str, FileReader]) -> FileReader:
    def reader(content: bytes) -> Iterator[tuple[str, TDataItems]]:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            for name in archive.namelist():
                path = Path(name)
                ext = path.suffix.lower()
                inner = (
                    reader if ext == ".zip" else readers.get(ext)
                )  # zip imbrique : recursion
                if inner is None:
                    continue
                stem = _to_snake(path.stem)
                for suffix, rows in inner(archive.read(name)):
                    yield (f"{stem}_{suffix}" if suffix else stem), rows

    return reader


def read_csv(
    content: bytes, separator: str = ";", encoding: str = "utf-8"
) -> Iterator[tuple[str, TDataItems]]:
    if encoding.lower().replace("-", "") != "utf8":
        content = content.decode(encoding).encode()
    yield (
        "",
        pl.read_csv(content, separator=separator, infer_schema_length=0).to_arrow(),
    )
