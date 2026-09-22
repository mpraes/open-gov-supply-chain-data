from typing import Any

from config.load_secret_key import load_secret_key_func
from etl.ingestion.arp.missing_keys import resolve_empenho_keys
from etl.ingestion.remaining_filters import arp_ata_header
from etl.ingestion.remaining_maps import map_arp_empenho_row
from etl.ingestion.remaining_query_params import arp_ata_query_params, slice_job_name
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH, _open_connection


def main() -> None:
    fallback = arp_ata_header(DEFAULT_ENV_PATH, load_secret_key_func)
    for ata_key, unidade_key in _empenho_keys(fallback):
        _ingest_empenho(ata_key, unidade_key)


def _empenho_keys(fallback: tuple[str, str] | None) -> list[tuple[str, str]]:
    conn = _open_connection(DEFAULT_ENV_PATH, load_secret_key_func, None)
    try:
        return resolve_empenho_keys(conn, fallback)
    finally:
        conn.close()


def _ingest_empenho(ata: str, unidade: str) -> int:
    return run_remaining_ingestion(
        logger_name="arp_empenho",
        endpoint_path="/modulo-arp/4_consultarEmpenhosSaldoItem",
        table_name="arp_empenho",
        map_row=lambda row: _map_empenho(row, ata, unidade),
        query_params=arp_ata_query_params(ata, unidade),
        job_name=slice_job_name("arp_empenho", ata, unidade),
    )


def _map_empenho(row: dict[str, Any], ata: str, unidade: str) -> Any:
    return map_arp_empenho_row(row, numero_ata=ata, unidade_gerenciadora=unidade)


if __name__ == "__main__":
    main()
