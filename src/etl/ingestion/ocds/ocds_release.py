from clients.compras_api import fetch_one_releases_page
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.full_dump import full_dump_dates
from etl.ingestion.orgao_catalog import read_buyer_cnpjs
from etl.ingestion.remaining_maps import map_ocds_release_row
from etl.ingestion.remaining_query_params import ocds_query_params
from etl.ingestion.remaining_run import run_sliced_remaining_ingestion


def main() -> None:
    inicial, final = full_dump_dates()
    for buyer in read_buyer_cnpjs():
        _ingest_buyer(buyer, inicial, final)


def _ingest_buyer(buyer: str, inicial: str, final: str) -> None:
    run_sliced_remaining_ingestion(
        data_inicial=inicial,
        data_final=final,
        params_for_slice=lambda start, end: ocds_query_params(buyer, start, end),
        job_prefix=f"ocds_release:{buyer}",
        logger_name="ocds_release",
        endpoint_path="/modulo-ocds/1_releases",
        table_name="ocds_release",
        map_row=map_ocds_release_row,
        fetch_page_fn=fetch_one_releases_page,
        date_watermark=DateWatermark(
            table="ocds_release",
            column="date",
            start_param="releaseStartDate",
            end_param="releaseEndDate",
            where={"buyer_id": buyer},
        ),
    )


if __name__ == "__main__":
    main()
