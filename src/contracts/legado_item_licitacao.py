from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_decimal
from contracts.text_normalize import strip_optional, upper_optional

_ID_FIELDS = ("id_compra", "id_compra_item")
_FLOAT_FIELDS = ("quantidade", "valor_estimado")
_NAME_FIELDS = (
    "numero_licitacao",
    "nome_uasg",
    "nome_modalidade",
    "nome_material",
    "nome_servico",
    "nome_fornecedor",
    "unidade",
    "descricao_item",
    "beneficio",
    "decreto_7174",
    "criterio_julgamento",
    "nome_vencedor_pf",
)
_CODE_FIELDS = ("cnpj_fornecedor", "cpf_vencedor")


class LegadoItemLicitacaoRecord(BaseModel):
    """Validated licitação item row from consultarItemLicitacao.

    Example:
        LegadoItemLicitacaoRecord(id_compra="c1", id_compra_item="i1")
    """

    model_config = ConfigDict(strict=True)

    numero_licitacao: str | None = None
    uasg: int | None = None
    nome_uasg: str | None = None
    modalidade: int | None = None
    nome_modalidade: str | None = None
    numero_aviso: int | None = None
    numero_item_licitacao: int | None = None
    codigo_item_material: int | None = None
    nome_material: str | None = None
    codigo_item_servico: int | None = None
    nome_servico: str | None = None
    cnpj_fornecedor: str | None = None
    nome_fornecedor: str | None = None
    quantidade: float | None = None
    unidade: str | None = None
    descricao_item: str | None = None
    beneficio: str | None = None
    valor_estimado: float | None = None
    decreto_7174: str | None = None
    criterio_julgamento: str | None = None
    cpf_vencedor: str | None = None
    nome_vencedor_pf: str | None = None
    sustentavel: int | None = None
    dt_alteracao: str | None = None
    id_compra: str
    id_compra_item: str

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

    @field_validator(*_CODE_FIELDS)
    @classmethod
    def optional_codes_strip(cls, value: str | None) -> str | None:
        return strip_optional(value)
