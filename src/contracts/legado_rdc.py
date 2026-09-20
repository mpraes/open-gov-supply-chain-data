from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_id_text
from contracts.text_normalize import upper_optional

_NAME_FIELDS = (
    "endereco_entrega_edital",
    "forma_de_realizacao_licitacao",
    "funcao_responsavel",
    "informacoes_gerais",
    "numero_processo",
    "objeto",
    "situacao_aviso",
    "tipo_recurso",
    "uf_uasg",
)


class LegadoRdcRecord(BaseModel):
    """Validated RDC row from consultarRdc.

    Example:
        LegadoRdcRecord(identificador="rdc-1", objeto="obra")
    """

    model_config = ConfigDict(strict=True)

    data_abertura_proposta: str | None = None
    data_entrega_edital: str | None = None
    data_entrega_proposta: str | None = None
    data_publicacao: str | None = None
    endereco_entrega_edital: str | None = None
    forma_de_realizacao_licitacao: str | None = None
    funcao_responsavel: str | None = None
    identificador: str
    informacoes_gerais: str | None = None
    modalidade: int | None = None
    nome_responsavel: str | None = None
    numero_aviso: int | None = None
    numero_itens: int | None = None
    numero_processo: str | None = None
    objeto: str | None = None
    situacao_aviso: str | None = None
    tipo_recurso: str | None = None
    uasg: int | None = None
    orgao_uasg: int | None = None
    uf_uasg: str | None = None

    @field_validator("identificador", mode="before")
    @classmethod
    def identity_text(cls, value: object, info: ValidationInfo) -> str:
        return coerce_id_text(value, info.field_name)

    @field_validator("nome_responsavel", mode="before")
    @classmethod
    def optional_nome_responsavel(cls, value: object) -> str | None:
        return coerce_optional_id_text(value, "nome_responsavel")

    @field_validator(*_NAME_FIELDS)
    @classmethod
    def optional_names_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
