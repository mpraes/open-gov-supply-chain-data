from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_optional


class ServicoNaturezaDespesaRecord(BaseModel):
    """Validated natureza-despesa row from consultarNaturezaDespesaServico.

    Example:
        ServicoNaturezaDespesaRecord(
            cod_servico=100, cod_natureza_despesa="339039",
            nome_natureza_despesa="servicos", status_natureza_despesa=True,
        )
    """

    model_config = ConfigDict(strict=True)

    cod_servico: int
    cod_natureza_despesa: str
    nome_natureza_despesa: str | None
    status_natureza_despesa: bool | None

    @field_validator("cod_natureza_despesa")
    @classmethod
    def codigo_non_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("cod_natureza_despesa must be non-empty")
        return cleaned

    @field_validator("nome_natureza_despesa")
    @classmethod
    def nome_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
