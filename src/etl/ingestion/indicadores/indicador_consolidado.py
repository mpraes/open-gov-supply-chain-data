from etl.ingestion.remaining_maps import map_indicador_consolidado_row
from etl.ingestion.remaining_run import run_remaining_ingestion


def main() -> None:
    run_remaining_ingestion(
        logger_name="indicador_consolidado",
        endpoint_path="/modulo-indicadores/1_consultarIndicadoresConsolidados",
        table_name="indicador_consolidado",
        map_row=map_indicador_consolidado_row,
        page_size=None,
    )


if __name__ == "__main__":
    main()
