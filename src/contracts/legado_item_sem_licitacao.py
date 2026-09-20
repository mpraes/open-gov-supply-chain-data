from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_decimal, coerce_optional_id_text
from contracts.text_normalize import strip_optional, upper_optional

_ID_FIELDS = ("id_compra", "id_compra_item")
_FLOAT_FIELDS = ("qt_material_alt", "vr_estimado", "vr_estimado_item")
_NAME_FIELDS = (
    "ds_detalhada",
    "in_tipo_fornecedor_vencedor",
    "no_fornecedor_vencedor",
    "no_conjunto_materiais",
    "no_marca_material",
    "no_servico",
    "no_unidade_medida",
    "in_material_servico",
    "no_modalidade_licitacao",
    "nu_inciso",
    "nu_processo",
    "ds_objeto_licitacao",
    "ds_fundamento_legal",
    "ds_justificativa",
    "no_responsavel_decl_disp",
    "no_cargo_resp_decl_disp",
    "no_responsavel_ratificacao",
    "no_cargo_resp_ratificacao",
    "ds_fabricante",
)
_CODE_FIELDS = (
    "nu_cnpj_vencedor",
    "nu_cpf_vencedor",
    "nu_cpf_resp_decl_disp",
    "nu_cpf_resp_ratificacao",
    "nu_cpf_resp_publicacao",
)


class LegadoItemSemLicitacaoRecord(BaseModel):
    """Validated dispensa item row from consultarCompraItensSemLicitacao.

    Example:
        LegadoItemSemLicitacaoRecord(id_compra="d1", id_compra_item="i2")
    """

    model_config = ConfigDict(strict=True)

    co_conjunto_materiais: int | None = None
    co_servico: int | None = None
    ds_detalhada: str | None = None
    in_tipo_fornecedor_vencedor: str | None = None
    no_fornecedor_vencedor: str | None = None
    no_conjunto_materiais: str | None = None
    no_marca_material: str | None = None
    no_servico: str | None = None
    no_unidade_medida: str | None = None
    nu_cnpj_vencedor: str | None = None
    nu_cpf_vencedor: str | None = None
    qt_material_alt: float | None = None
    vr_estimado: float | None = None
    in_material_servico: str | None = None
    dt_publicacao: str | None = None
    id_compra: str
    id_compra_item: str
    co_uasg: int | None = None
    co_modalidade_licitacao: int | None = None
    no_modalidade_licitacao: str | None = None
    nu_aviso_licitacao: int | None = None
    dt_ano_aviso_licitacao: int | None = None
    nu_inciso: str | None = None
    nu_processo: str | None = None
    qt_total_item: int | None = None
    ds_objeto_licitacao: str | None = None
    ds_fundamento_legal: str | None = None
    ds_justificativa: str | None = None
    nu_cpf_resp_decl_disp: str | None = None
    nu_cpf_resp_ratificacao: str | None = None
    nu_cpf_resp_publicacao: str | None = None
    no_responsavel_decl_disp: str | None = None
    no_cargo_resp_decl_disp: str | None = None
    no_responsavel_ratificacao: str | None = None
    no_cargo_resp_ratificacao: str | None = None
    nu_item_material: int | None = None
    vr_estimado_item: float | None = None
    ds_fabricante: str | None = None
    dt_alteracao: str | None = None
    co_orgao: str | None = None

    @field_validator(*_ID_FIELDS, mode="before")
    @classmethod
    def identity_text(cls, value: object, info: ValidationInfo) -> str:
        return coerce_id_text(value, info.field_name)

    @field_validator("co_orgao", mode="before")
    @classmethod
    def optional_orgao(cls, value: object) -> str | None:
        return coerce_optional_id_text(value, "co_orgao")

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
