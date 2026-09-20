import inspect

from etl.ingestion.precos import preco_material, preco_material_detalhe
from etl.ingestion.precos import preco_servico, preco_servico_detalhe
from etl.ingestion.precos.batch_runner import run_preco_batch_ingestion
from etl.ingestion.precos.code_pages import build_codigo_fetch_pages


def test_preco_batch_ingestion_does_not_pause_between_codes() -> None:
    pause = inspect.signature(run_preco_batch_ingestion).parameters["pause_seconds"]
    assert pause.default == 0


def test_build_codigo_fetch_pages_does_not_pause_by_default() -> None:
    pause = inspect.signature(build_codigo_fetch_pages).parameters["pause_seconds"]
    assert pause.default == 0


def test_preco_material_walks_pdm_codes_with_new_job() -> None:
    assert preco_material.CATALOG_TABLE == "material_pdm"
    assert preco_material.CATALOG_COLUMN == "cod_pdm"
    assert preco_material.JOB_NAME == "preco_material_pdm"
    assert preco_material.PAGE_SIZE == 500


def test_preco_scripts_use_page_size_500() -> None:
    assert preco_material_detalhe.PAGE_SIZE == 500
    assert preco_servico.PAGE_SIZE == 500
    assert preco_servico_detalhe.PAGE_SIZE == 500
