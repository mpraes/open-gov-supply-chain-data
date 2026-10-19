"""Ingere itens de contratação PNCP na tabela contratacao_item."""

from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import contratacoes_dates
from etl.ingestion.remaining_maps import map_contratacao_item_row
from etl.ingestion.remaining_query_params import contratacao_item_query_params
from etl.ingestion.remaining_run import run_sliced_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    """Lê o intervalo de datas e consulta /modulo-contratacoes/2_consultarItensContratacoes_PNCP_14133 em fatias de inclusão PNCP, gravando na tabela contratacao_item."""
    inicial, final = contratacoes_dates(DEFAULT_ENV_PATH, load_secret_key_func)
    run_sliced_remaining_ingestion(
        data_inicial=inicial,
        data_final=final,
        params_for_slice=contratacao_item_query_params,
        job_prefix="contratacao_item",
        logger_name="contratacao_item",
        endpoint_path="/modulo-contratacoes/2_consultarItensContratacoes_PNCP_14133",
        table_name="contratacao_item",
        map_row=map_contratacao_item_row,
        date_watermark=DateWatermark(
            table="contratacao_item",
            column="data_inclusao_pncp",
            start_param="dataInclusaoPncpInicial",
            end_param="dataInclusaoPncpFinal",
        ),
    )


if __name__ == "__main__":
    main()
