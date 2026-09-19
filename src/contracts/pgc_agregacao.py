from pydantic import BaseModel, ConfigDict, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_float
from contracts.text_normalize import upper_optional


class PgcAgregacaoRecord(BaseModel):
    """Validated PGC aggregation row from consultarPgcAgregacao.

    Example:
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
        return coerce_id_text(value, "orgao")

    @field_validator("valor_total_estimado", mode="before")
    @classmethod
    def optional_valor(cls, value: object) -> float | None:
        return coerce_optional_float(value)

    @field_validator("poder", "esfera")
    @classmethod
    def optional_names_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
