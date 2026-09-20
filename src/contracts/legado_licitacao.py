from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_decimal
from contracts.text_normalize import upper_optional

_ID_FIELDS = ("id_compra",)
_FLOAT_FIELDS = ("valor_estimado_total", "valor_homologado_total")
_NAME_FIELDS = (
    "identificador",
    "numero_processo",
    "nome_modalidade",
    "situacao_aviso",
    "tipo_pregao",
    "tipo_recurso",
    "nome_responsavel",
    "funcao_responsavel",
    "informacoes_gerais",
    "objeto",
    "endereco_entrega_edital",
)


class LegadoLicitacaoRecord(BaseModel):
    """Validated licitação row from consultarLicitacao.

    Example:
        LegadoLicitacaoRecord(id_compra="123", objeto="notebook")
    """

    model_config = ConfigDict(strict=True)

    id_compra: str
    identificador: str | None = None
    numero_processo: str | None = None
    uasg: int | None = None
    modalidade: int | None = None
    nome_modalidade: str | None = None
    numero_aviso: int | None = None
    situacao_aviso: str | None = None
    tipo_pregao: str | None = None
    tipo_recurso: str | None = None
    nome_responsavel: str | None = None
    funcao_responsavel: str | None = None
    numero_itens: int | None = None
    valor_estimado_total: float | None = None
    valor_homologado_total: float | None = None
    informacoes_gerais: str | None = None
    objeto: str | None = None
    endereco_entrega_edital: str | None = None
    codigo_municipio_uasg: int | None = None
    data_abertura_proposta: str | None = None
    data_entrega_edital: str | None = None
    data_entrega_proposta: str | None = None
    data_publicacao: str | None = None
    dt_alteracao: str | None = None
    pertence14133: bool | None = None

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
