"""Ingere unidades de item de ata na tabela arp_unidade_item."""

from config.load_secret_key import load_secret_key_func
from etl.ingestion.arp.missing_keys import resolve_item_keys
from etl.ingestion.remaining_maps import map_arp_unidade_row
from etl.ingestion.remaining_query_params import arp_ata_query_params, slice_job_name
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH, _open_connection

CHILD_TABLE = "arp_unidade_item"


def main() -> None:
    """Consulta /modulo-arp/3_consultarUnidadesItem para cada chave de item ausente e grava na tabela arp_unidade_item."""
    for ata, unidade, item in _item_keys():
        _ingest_unidade(ata, unidade, item)


def _item_keys() -> list[tuple[str, str, str]]:
    """Abre a conexão, resolve as chaves de item ausentes em arp_unidade_item e fecha a conexão."""
    conn = _open_connection(DEFAULT_ENV_PATH, load_secret_key_func, None)
    try:
        return resolve_item_keys(conn, CHILD_TABLE, None)
    finally:
        conn.close()


def _ingest_unidade(ata: str, unidade: str, item: str) -> int:
    """Consulta /modulo-arp/3_consultarUnidadesItem da ata, da unidade e do item e devolve a quantidade de registros ingeridos."""
    return run_remaining_ingestion(
        logger_name="arp_unidade_item",
        endpoint_path="/modulo-arp/3_consultarUnidadesItem",
        table_name=CHILD_TABLE,
        map_row=map_arp_unidade_row,
        query_params=arp_ata_query_params(ata, unidade, item),
        job_name=slice_job_name("arp_unidade_item", ata, unidade, item),
    )


if __name__ == "__main__":
    main()
