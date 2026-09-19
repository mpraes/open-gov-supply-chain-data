import pytest
from pydantic import ValidationError

from contracts.servico_divisao import ServicoDivisaoRecord
from contracts.servico_grupo import ServicoGrupoRecord
from contracts.servico_classe import ServicoClasseRecord
from contracts.servico_subclasse import ServicoSubclasseRecord
from contracts.servico_item import ServicoItemRecord
from contracts.servico_unidade_medida import ServicoUnidadeMedidaRecord
from contracts.servico_natureza_despesa import ServicoNaturezaDespesaRecord


def test_servico_divisao_uppercases_nomes() -> None:
    record = ServicoDivisaoRecord(
        cod_divisao=2,
        cod_secao=1,
        nome_secao=" secao ",
        nome_divisao=" divisao ",
        status_divisao=True,
        data_hora_atualizacao="2024-01-15T10:30:00",
    )
    assert record.nome_secao == "SECAO"
    assert record.nome_divisao == "DIVISAO"


def test_servico_grupo_uppercases_nomes() -> None:
    record = ServicoGrupoRecord(
        cod_grupo=3,
        cod_divisao=2,
        nome_secao="s",
        nome_divisao="d",
        nome_grupo=" grupo ",
        status_grupo=True,
        data_hora_atualizacao="2024-01-15T10:30:00",
    )
    assert record.nome_grupo == "GRUPO"


def test_servico_grupo_accepts_null_nome_secao() -> None:
    # API sometimes returns nomeSecao=null (e.g. codigoGrupo=111).
    record = ServicoGrupoRecord(
        cod_grupo=111,
        cod_divisao=11,
        nome_secao=None,
        nome_divisao="divisao",
        nome_grupo="grupo",
        status_grupo=True,
        data_hora_atualizacao="2021-10-16T09:07:04.535092",
    )
    assert record.nome_secao is None
    assert record.nome_grupo == "GRUPO"


def test_servico_classe_uppercases_nomes() -> None:
    record = ServicoClasseRecord(
        cod_classe=4,
        cod_grupo=3,
        nome_grupo="g",
        nome_classe=" classe ",
        status_classe=True,
        data_hora_atualizacao="2024-01-15T10:30:00",
    )
    assert record.nome_classe == "CLASSE"


def test_servico_subclasse_uppercases_nomes() -> None:
    record = ServicoSubclasseRecord(
        cod_subclasse=5,
        cod_classe=4,
        nome_classe="c",
        nome_subclasse=" sub ",
        status_subclasse=True,
        data_hora_atualizacao="2024-01-15T10:30:00",
    )
    assert record.nome_subclasse == "SUB"


def test_servico_item_uppercases_nome_servico() -> None:
    record = ServicoItemRecord(
        cod_servico=100,
        cod_secao=1,
        nome_secao="s",
        cod_divisao=2,
        nome_divisao="d",
        cod_grupo=3,
        nome_grupo="g",
        cod_classe=4,
        nome_classe="c",
        cod_subclasse=5,
        nome_subclasse="sc",
        nome_servico=" servico x ",
        cod_cpc=9,
        exclusivo_central_compras=False,
        status_servico=True,
        data_hora_atualizacao="2024-01-15T10:30:00",
    )
    assert record.nome_servico == "SERVICO X"


def test_servico_item_accepts_null_subclasse() -> None:
    # API sometimes omits subclasse (e.g. codigoServico=7250).
    record = ServicoItemRecord(
        cod_servico=7250,
        cod_secao=9,
        nome_secao="s",
        cod_divisao=93,
        nome_divisao="d",
        cod_grupo=931,
        nome_grupo="g",
        cod_classe=9311,
        nome_classe="c",
        cod_subclasse=None,
        nome_subclasse=None,
        nome_servico="endoscopia",
        cod_cpc=9311,
        exclusivo_central_compras=False,
        status_servico=True,
        data_hora_atualizacao="2021-10-16T09:09:59.689615",
    )
    assert record.cod_subclasse is None
    assert record.nome_subclasse is None


def test_servico_item_accepts_null_classe() -> None:
    # API sometimes omits classe+subclasse (e.g. codigoServico=2488).
    record = ServicoItemRecord(
        cod_servico=2488,
        cod_secao=8,
        nome_secao="s",
        cod_divisao=87,
        nome_divisao="d",
        cod_grupo=871,
        nome_grupo="g",
        cod_classe=None,
        nome_classe=None,
        cod_subclasse=None,
        nome_subclasse=None,
        nome_servico="manutencao",
        cod_cpc=871,
        exclusivo_central_compras=False,
        status_servico=True,
        data_hora_atualizacao="2021-10-16T09:09:59.689615",
    )
    assert record.cod_classe is None
    assert record.nome_classe is None


def test_servico_item_rejects_non_int_cod_servico() -> None:
    with pytest.raises(ValidationError):
        ServicoItemRecord(
            cod_servico="100",  # type: ignore[arg-type]
            cod_secao=1,
            nome_secao="s",
            cod_divisao=2,
            nome_divisao="d",
            cod_grupo=3,
            nome_grupo="g",
            cod_classe=4,
            nome_classe="c",
            cod_subclasse=5,
            nome_subclasse="sc",
            nome_servico="x",
            cod_cpc=None,
            exclusivo_central_compras=None,
            status_servico=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )


def test_servico_unidade_medida_uppercases_sigla() -> None:
    record = ServicoUnidadeMedidaRecord(
        cod_servico=100,
        sigla_unidade_medida=" un ",
        nome_unidade_medida=" unidade ",
        status_unidade_medida=True,
    )
    assert record.sigla_unidade_medida == "UN"
    assert record.nome_unidade_medida == "UNIDADE"


def test_servico_natureza_despesa_strips_codigo() -> None:
    record = ServicoNaturezaDespesaRecord(
        cod_servico=100,
        cod_natureza_despesa=" 339039 ",
        nome_natureza_despesa=" servicos ",
        status_natureza_despesa=True,
    )
    assert record.cod_natureza_despesa == "339039"
    assert record.nome_natureza_despesa == "SERVICOS"
