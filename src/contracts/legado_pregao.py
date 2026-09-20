from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_decimal
from contracts.text_normalize import upper_optional

_FLOAT_FIELDS = ("valor_estimado_total", "valor_homologado_total")
_NAME_FIELDS = (
    "co_processo",
    "co_portaria",
    "no_ausg",
    "no_orgao",
    "ds_situacao_pregao",
    "ds_tipo_pregao",
    "ds_tipo_pregao_compra",
    "tx_objeto",
)


class LegadoPregaoRecord(BaseModel):
    """Validated pregão row from consultarPregoes.

    Example:
        LegadoPregaoRecord(id_compra="p1", valor_estimado_total="1.5")
    """

    model_config = ConfigDict(strict=True)

    id_compra: str
    co_processo: str | None = None
    co_portaria: str | None = None
    co_uasg: int | None = None
    no_ausg: str | None = None
    co_orgao: int | None = None
    no_orgao: str | None = None
    numero: int | None = None
    ds_situacao_pregao: str | None = None
    ds_tipo_pregao: str | None = None
    ds_tipo_pregao_compra: str | None = None
    tx_objeto: str | None = None
    valor_estimado_total: float | None = None
    valor_homologado_total: float | None = None
    dt_portaria: str | None = None
    dt_data_edital: str | None = None
    dt_inicio_proposta: str | None = None
    dt_fim_proposta: str | None = None
    dt_alteracao: str | None = None
    dt_encerramento: str | None = None
    dt_resultado: str | None = None
    pertence14133: bool | None = None

    @field_validator("id_compra", mode="before")
    @classmethod
    def identity_text(cls, value: object, info: ValidationInfo) -> str:
        return coerce_id_text(value, info.field_name)

    @field_validator(*_FLOAT_FIELDS, mode="before")
    @classmethod
    def optional_amounts(cls, value: object) -> float | None:
        return coerce_optional_decimal(value)

    @field_validator(*_NAME_FIELDS)
    @classmethod
    def optional_names_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
