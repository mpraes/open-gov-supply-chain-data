"""Contrato da linha de natureza de despesa de consultarNaturezaDespesaServico."""

from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_optional


class ServicoNaturezaDespesaRecord(BaseModel):
    """Linha validada de natureza de despesa de consultarNaturezaDespesaServico.

    Exemplo:
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
        """Rejeita cod_natureza_despesa vazio e devolve o texto sem espaços nas bordas."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("cod_natureza_despesa must be non-empty")
        return cleaned

    @field_validator("nome_natureza_despesa")
    @classmethod
    def nome_upper(cls, value: str | None) -> str | None:
        """Converte nome_natureza_despesa para maiúsculas; vazio vira None."""
        return upper_optional(value)
