from config.load_secret_key import load_secret_key_func
from etl.ingestion.arp.missing_keys import resolve_item_keys
from etl.ingestion.remaining_filters import arp_ata_keys
from etl.ingestion.remaining_maps import map_arp_adesao_row
from etl.ingestion.remaining_query_params import arp_ata_query_params, slice_job_name
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH, _open_connection

CHILD_TABLE = "arp_adesao"


def main() -> None:
    fallback = arp_ata_keys(DEFAULT_ENV_PATH, load_secret_key_func)
    for ata, unidade, item in _item_keys(fallback):
        _ingest_adesao(ata, unidade, item)


def _item_keys(fallback: tuple[str, str, str] | None) -> list[tuple[str, str, str]]:
    conn = _open_connection(DEFAULT_ENV_PATH, load_secret_key_func, None)
    try:
        return resolve_item_keys(conn, CHILD_TABLE, fallback)
    finally:
        conn.close()


def _ingest_adesao(ata: str, unidade: str, item: str) -> int:
    return run_remaining_ingestion(
        logger_name="arp_adesao",
        endpoint_path="/modulo-arp/5_consultarAdesoesItem",
        table_name=CHILD_TABLE,
        map_row=map_arp_adesao_row,
        query_params=arp_ata_query_params(ata, unidade, item),
        job_name=slice_job_name("arp_adesao", ata, unidade, item),
    )


if __name__ == "__main__":
    main()
