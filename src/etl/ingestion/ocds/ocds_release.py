from clients.compras_api import fetch_one_releases_page
from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import ocds_buyer_dates
from etl.ingestion.remaining_maps import map_ocds_release_row
from etl.ingestion.remaining_query_params import ocds_query_params, slice_job_name
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    buyer, inicial, final = ocds_buyer_dates(DEFAULT_ENV_PATH, load_secret_key_func)
    run_remaining_ingestion(
        logger_name="ocds_release",
        endpoint_path="/modulo-ocds/1_releases",
        table_name="ocds_release",
        map_row=map_ocds_release_row,
        query_params=ocds_query_params(buyer, inicial, final),
        job_name=slice_job_name("ocds_release", buyer, inicial, final),
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
