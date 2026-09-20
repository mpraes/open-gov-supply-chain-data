from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_decimal
from contracts.text_normalize import upper_optional

_ID_FIELDS = ("id_compra", "id_compra_item")
_FLOAT_FIELDS = (
    "quantidade_item",
    "valor_estimado_item",
    "menor_lance",
    "valor_negociado",
    "valor_homologado_item",
)
_NAME_FIELDS = (
    "decreto_7174",
    "situacao_item",
    "descricao_item",
    "descricao_detalhada_item",
    "margem_preferencial",
    "tratamento_diferenciado",
    "unidade_fornecimento",
    "fornecedor_vencedor",
    "no_adjudic",
    "no_hom",
)


class LegadoItemPregaoRecord(BaseModel):
    """Validated pregão item row from consultarItensPregoes.

    Example:
        LegadoItemPregaoRecord(id_compra="p1", id_compra_item="i1")
    """

    model_config = ConfigDict(strict=True)

    id_compra: str
    id_compra_item: str
    decreto_7174: str | None = None
    situacao_item: str | None = None
    descricao_item: str | None = None
    descricao_detalhada_item: str | None = None
    margem_preferencial: str | None = None
    tratamento_diferenciado: str | None = None
    quantidade_item: float | None = None
    unidade_fornecimento: str | None = None
    valor_estimado_item: float | None = None
    menor_lance: float | None = None
    valor_negociado: float | None = None
    valor_homologado_item: float | None = None
    fornecedor_vencedor: str | None = None
    no_adjudic: str | None = None
    no_hom: str | None = None
    dt_encerramento: str | None = None
    dt_adjudic: str | None = None
    dt_hom: str | None = None
    dt_alteracao: str | None = None

    @field_validator(*_ID_FIELDS, mode="before")
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
