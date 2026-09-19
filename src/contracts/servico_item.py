from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_non_empty, upper_optional


class ServicoItemRecord(BaseModel):
    """Validated item row from consultarItemServico.

    Example:
        ServicoItemRecord(
            cod_servico=100, cod_secao=1, nome_secao="s", cod_divisao=2,
            nome_divisao="d", cod_grupo=3, nome_grupo="g", cod_classe=4,
            nome_classe="c", cod_subclasse=5, nome_subclasse="sc",
            nome_servico="servico", cod_cpc=9, exclusivo_central_compras=False,
            status_servico=True, data_hora_atualizacao="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_servico: int
    # Hierarchy fields are often partially null in real API payloads.
    cod_secao: int | None
    nome_secao: str | None
    cod_divisao: int | None
    nome_divisao: str | None
    cod_grupo: int | None
    nome_grupo: str | None
    cod_classe: int | None
    nome_classe: str | None
    cod_subclasse: int | None
    nome_subclasse: str | None
    nome_servico: str
    cod_cpc: int | None
    exclusivo_central_compras: bool | None
    status_servico: bool
    data_hora_atualizacao: str

    @field_validator("nome_servico")
    @classmethod
    def nome_servico_upper(cls, value: str) -> str:
        return upper_non_empty(value, "nome_servico")

    @field_validator(
        "nome_secao",
        "nome_divisao",
        "nome_grupo",
        "nome_classe",
        "nome_subclasse",
    )
    @classmethod
    def optional_nomes_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
