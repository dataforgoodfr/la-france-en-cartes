import dlt
from dlt.destinations.impl.filesystem.filesystem import FilesystemClient
from dlt.sources import DltSource


def _loaded_resources(pipeline: dlt.Pipeline, source_name: str) -> set[str]:
    """Ressources dont toutes les tables ont deja un parquet dans la destination."""
    if source_name not in pipeline.schema_names:
        return set()

    tables: dict[str, list[str]] = {}
    for table in pipeline.schemas[source_name].data_tables(seen_data_only=True):
        resource, name = table.get("resource"), table.get("name")
        if resource is None or name is None:
            continue
        tables.setdefault(resource, []).append(name)

    client = pipeline.destination_client()
    if not isinstance(client, FilesystemClient):
        raise TypeError(
            f"destination filesystem attendue, recu {type(client).__name__}"
        )
    fs, base = client.fs_client, client.dataset_path

    def has_parquet(table: str) -> bool:
        return bool(
            fs.glob(f"{base}{table}/*.parquet") or fs.glob(f"{base}{table}.parquet")
        )

    return {
        resource
        for resource, names in tables.items()
        if all(has_parquet(n) for n in names)
    }


def run_pipeline(domain: str, *sources: DltSource, force: bool = False) -> None:
    """Charge les sources du domaine ; saute les ressources deja en parquet sauf si force=True."""
    pipeline = dlt.pipeline(
        pipeline_name=domain, destination="filesystem", dataset_name=domain
    )
    pipeline.sync_destination()  # etat depuis la destination

    for source in sources:
        if not force:
            loaded = _loaded_resources(pipeline, source.name)
            todo = [name for name in source.resources if name not in loaded]
            for name in sorted(loaded & set(source.resources)):
                print(
                    f"{source.name}.{name} : parquet existant, skip (force=True pour recharger)"
                )
            if not todo:
                continue
            source = source.with_resources(*todo)

        load_info = pipeline.run(source, loader_file_format="parquet")
        load_info.raise_on_failed_jobs()
        print(load_info)
