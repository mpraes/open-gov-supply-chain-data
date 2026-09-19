from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_non_empty, upper_optional


class ServicoUnidadeMedidaRecord(BaseModel):
    """Validated unidade-medida row from consultarUndMedidaServico.

    Example:
        ServicoUnidadeMedidaRecord(
            cod_servico=100, sigla_unidade_medida="un",
            nome_unidade_medida="unidade", status_unidade_medida=True,
        )
    """

    model_config = ConfigDict(strict=True)

    cod_servico: int
    sigla_unidade_medida: str
    nome_unidade_medida: str | None
    status_unidade_medida: bool | None

    @field_validator("sigla_unidade_medida")
    @classmethod
    def sigla_upper(cls, value: str) -> str:
        return upper_non_empty(value, "sigla_unidade_medida")

    @field_validator("nome_unidade_medida")
    @classmethod
    def nome_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
