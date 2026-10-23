"""Trava o filtro orgao do PGC no CNPJ do comprador, não no código SIASG."""

from collections.abc import Callable

from pytest import MonkeyPatch

from etl.ingestion.planejamento.pgc_agregacao import main as agregacao_main
from etl.ingestion.planejamento.pgc_detalhe import main as detalhe_main


class SiasgCodes:
    """Devolve um código SIASG se a carga ainda ler uasg_orgao.codigo_orgao."""

    def __call__(self) -> list[int]:
        """Retorna o código SIASG da UFU."""
        return [26274]


class BuyerCnpjs:
    """Devolve o CNPJ sem máscara que a API de PGC espera em orgao."""

    def __call__(self) -> list[str]:
        """Retorna o CNPJ da UFU."""
        return ["25648387000118"]


class OneDumpYear:
    """Substitui a janela completa por um único ano."""

    def __init__(self, ano: int) -> None:
        """Guarda o ano que visit vai receber."""
        self._ano = ano

    def __call__(self, visit: Callable[[int], None], **_kwargs: object) -> None:
        """Chama visit uma vez com o ano guardado."""
        visit(self._ano)


class CapturedPageRun:
    """Guarda os argumentos de cada carga de página."""

    def __init__(self) -> None:
        """Começa sem chamadas registradas."""
        self.calls: list[dict[str, object]] = []

    def __call__(self, **kwargs: object) -> int:
        """Registra a chamada e devolve zero linhas gravadas."""
        self.calls.append(kwargs)
        return 0


def test_pgc_detalhe_main_filters_by_buyer_cnpj(monkeypatch: MonkeyPatch) -> None:
    captured = CapturedPageRun()
    _patch_buyer_dump(
        monkeypatch,
        "etl.ingestion.planejamento.pgc_detalhe",
        captured,
    )
    detalhe_main()
    assert captured.calls[0]["query_params"] == {
        "orgao": "25648387000118",
        "anoPcaProjetoCompra": 2025,
    }
    assert captured.calls[0]["job_name"] == "pgc_detalhe:25648387000118:2025"


def test_pgc_agregacao_main_filters_by_buyer_cnpj(monkeypatch: MonkeyPatch) -> None:
    captured = CapturedPageRun()
    _patch_buyer_dump(
        monkeypatch,
        "etl.ingestion.planejamento.pgc_agregacao",
        captured,
    )
    agregacao_main()
    assert captured.calls[0]["query_params"] == {
        "orgao": "25648387000118",
        "ano": 2025,
    }
    assert captured.calls[0]["job_name"] == "pgc_agregacao:25648387000118:2025"


def _patch_buyer_dump(monkeypatch: MonkeyPatch, module: str, captured: CapturedPageRun) -> None:
    """Isola a carga: código SIASG disponível, CNPJ injetado e um único ano."""
    monkeypatch.setattr(f"{module}.read_orgao_codes", SiasgCodes(), raising=False)
    monkeypatch.setattr(f"{module}.read_buyer_cnpjs", BuyerCnpjs(), raising=False)
    monkeypatch.setattr(f"{module}.for_each_dump_year", OneDumpYear(2025))
    monkeypatch.setattr(f"{module}.run_page_batch_ingestion", captured)
