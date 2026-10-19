"""Contrato da linha de agregação do PGC de consultarPgcAgregacao."""

from pydantic import BaseModel, ConfigDict, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_float
from contracts.text_normalize import upper_optional


class PgcAgregacaoRecord(BaseModel):
    """Linha validada de agregação do PGC de consultarPgcAgregacao.

    Exemplo:
        PgcAgregacaoRecord(orgao="36000", ano=2026, valor_total_estimado=10.5)
    """

    model_config = ConfigDict(strict=True)

    orgao: str
    ano: int
    poder: str | None = None
    esfera: str | None = None
    data_hora_publicacao_pncp: str | None = None
    data_hora_atualizacao: str | None = None
    quantidade_total_itens: int | None = None
    valor_total_estimado: float | None = None

    @field_validator("orgao", mode="before")
    @classmethod
    def orgao_text(cls, value: object) -> str:
        """Converte orgao int ou str em texto sem espaços nas bordas."""
        return coerce_id_text(value, "orgao")

    @field_validator("valor_total_estimado", mode="before")
    @classmethod
    def optional_valor(cls, value: object) -> float | None:
        """Coage valor_total_estimado para float; None permanece None e bool é rejeitado."""
        return coerce_optional_float(value)

    @field_validator("poder", "esfera")
    @classmethod
    def optional_names_upper(cls, value: str | None) -> str | None:
        """Converte poder e esfera para maiúsculas; vazio vira None."""
        return upper_optional(value)
