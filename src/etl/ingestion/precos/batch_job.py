from collections.abc import Mapping
from dataclasses import dataclass
from logging import Logger

from clients.compras_api import CodeParamsFn
from etl.ingestion.pipeline import MapRow, SupportsDbConnection
from etl.ingestion.precos.code_pages import FetchForCodes


@dataclass(frozen=True)
class PrecoFetchSpec:
    url: str
    headers: dict[str, str]
    page_size: int | None
    upsert_sql: str
    map_row: MapRow
    table_name: str
    pause_seconds: float
    parallel_codes: int
    fetch_for_codes: FetchForCodes


@dataclass(frozen=True)
class PrecoCatalogSpec:
    catalog_table: str
    catalog_column: str
    params_for_code: CodeParamsFn
    dest_code_column: str | None
    stringify_code: bool
    dest_date_column: str
    absent_dest_table: str | None
    absent_dest_column: str | None
    absent_filters: Mapping[str, str | int] | None
    batch_size: int
    job_name: str


@dataclass(frozen=True)
class PrecoBatchJob:
    conn: SupportsDbConnection
    log: Logger
    fetch: PrecoFetchSpec
    catalog: PrecoCatalogSpec
