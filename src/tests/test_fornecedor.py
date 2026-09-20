import inspect

from etl.ingestion.fornecedor import fornecedor
from etl.ingestion.remaining_query_params import slice_job_name


def test_fornecedor_uses_page_size_500_and_limited_parallel() -> None:
    assert fornecedor.PAGE_SIZE == 500
    assert fornecedor.PARALLEL_PAGES == 4
    assert slice_job_name("fornecedor", "true", fornecedor.PAGE_SIZE) == "fornecedor:true:500"


def test_fornecedor_main_opts_into_parallel_fetch() -> None:
    src = inspect.getsource(fornecedor.main)
    assert "page_size=PAGE_SIZE" in src
    assert "parallel_pages=PARALLEL_PAGES" in src
    assert "slice_job_name(\"fornecedor\", str(ativo).lower(), PAGE_SIZE)" in src
