from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import contratacoes_date_modalidade
from etl.ingestion.remaining_maps import map_contratacao_row
from etl.ingestion.remaining_query_params import contratacao_query_params, slice_job_name
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    inicial, final, modalidade = contratacoes_date_modalidade(
        DEFAULT_ENV_PATH, load_secret_key_func
    )
    run_remaining_ingestion(
        logger_name="contratacao",
        endpoint_path="/modulo-contratacoes/1_consultarContratacoes_PNCP_14133",
        table_name="contratacao",
        map_row=map_contratacao_row,
        query_params=contratacao_query_params(inicial, final, modalidade),
        job_name=slice_job_name("contratacao", inicial, final, modalidade),
        date_watermark=DateWatermark(
            table="contratacao",
            column="data_publicacao_pncp",
            start_param="dataPublicacaoPncpInicial",
            end_param="dataPublicacaoPncpFinal",
            where={"codigo_modalidade": str(modalidade)},
        ),
    )


if __name__ == "__main__":
    main()
