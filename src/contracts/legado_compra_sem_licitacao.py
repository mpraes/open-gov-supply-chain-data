from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_decimal, coerce_optional_id_text
from contracts.text_normalize import upper_optional

_FLOAT_FIELDS = ("vr_estimado",)
_NAME_FIELDS = (
    "no_ausg",
    "ds_lei",
    "nu_processo",
    "ds_objeto_licitacao",
    "ds_fundamento_legal",
    "ds_justificativa",
    "no_responsavel_decl_disp",
    "no_cargo_resp_decl_disp",
    "no_responsavel_ratificacao",
    "no_cargo_resp_ratificacao",
)
_CODE_FIELDS = ("co_orgao", "co_orgao_superior")


class LegadoCompraSemLicitacaoRecord(BaseModel):
    """Validated dispensa row from consultarComprasSemLicitacao.

    Example:
        LegadoCompraSemLicitacaoRecord(id_compra="d1", ds_objeto_licitacao="x")
    """

    model_config = ConfigDict(strict=True)

    id_compra: str
    co_orgao: str | None = None
    co_orgao_superior: str | None = None
    co_uasg: int | None = None
    no_ausg: str | None = None
    co_modalidade_licitacao: int | None = None
    ds_lei: str | None = None
    nu_processo: str | None = None
    qt_total_item: int | None = None
    vr_estimado: float | None = None
    nu_aviso_licitacao: int | None = None
    ds_objeto_licitacao: str | None = None
    ds_fundamento_legal: str | None = None
    ds_justificativa: str | None = None
    no_responsavel_decl_disp: str | None = None
    no_cargo_resp_decl_disp: str | None = None
    no_responsavel_ratificacao: str | None = None
    no_cargo_resp_ratificacao: str | None = None
    dt_declaracao_dispensa: str | None = None
    dt_ratificacao: str | None = None
    dt_publicacao: str | None = None
    dt_ano_aviso: int | None = None
    dt_alteracao: str | None = None
    pertence14133: bool | None = None

    @field_validator("id_compra", mode="before")
    @classmethod
    def identity_text(cls, value: object, info: ValidationInfo) -> str:
        return coerce_id_text(value, info.field_name)

    @field_validator(*_CODE_FIELDS, mode="before")
    @classmethod
    def optional_codes(cls, value: object, info: ValidationInfo) -> str | None:
        return coerce_optional_id_text(value, info.field_name)

    @field_validator(*_FLOAT_FIELDS, mode="before")
    @classmethod
    def optional_amounts(cls, value: object) -> float | None:
        return coerce_optional_decimal(value)

    @field_validator(*_NAME_FIELDS)
    @classmethod
    def optional_names_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
