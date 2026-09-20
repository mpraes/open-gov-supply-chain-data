from etl.ingestion.remaining_maps import map_fornecedor_row
from etl.ingestion.remaining_query_params import fornecedor_query_params, slice_job_name
from etl.ingestion.remaining_run import run_remaining_ingestion


def main() -> None:
    for ativo in (True, False):
        run_remaining_ingestion(
            logger_name="fornecedor",
            endpoint_path="/modulo-fornecedor/1_consultarFornecedor",
            table_name="fornecedor",
            map_row=map_fornecedor_row,
            query_params=fornecedor_query_params(ativo),
            job_name=slice_job_name("fornecedor", str(ativo).lower()),
        )


if __name__ == "__main__":
    main()
