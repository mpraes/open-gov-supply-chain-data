from pydantic import BaseModel, ConfigDict, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_float
from contracts.text_normalize import upper_optional

_FLOAT_FIELDS = (
    "quantidade",
    "preco_unitario",
    "percentual_maior_desconto",
)

_NAME_FIELDS = (
    "forma",
    "descricao_item",
    "nome_unidade_medida",
    "sigla_unidade_medida",
    "criterio_julgamento",
    "ni_fornecedor",
    "nome_fornecedor",
    "codigo_uasg",
    "nome_uasg",
    "municipio",
    "estado",
    "nome_orgao",
    "poder",
    "esfera",
    "objeto_compra",
    "descricao_detalhada_item",
)


class PrecoServicoRecord(BaseModel):
    """Validated price row from consultarServico.

    Example:
        PrecoServicoRecord(
            id_compra="c1", id_item_compra=1, codigo_item_catalogo=7250,
            descricao_item="servico", preco_unitario=1.5,
        )
    """

    model_config = ConfigDict(strict=True)

    id_compra: str
    id_item_compra: int
    numero_item_compra: int | None = None
    codigo_item_catalogo: int
    forma: str | None = None
    modalidade: int | None = None
    criterio_julgamento: str | None = None
    descricao_item: str | None = None
    nome_unidade_medida: str | None = None
    sigla_unidade_medida: str | None = None
    quantidade: float | None = None
    preco_unitario: float | None = None
    percentual_maior_desconto: float | None = None
    ni_fornecedor: str | None = None
    nome_fornecedor: str | None = None
    codigo_uasg: str | None = None
    nome_uasg: str | None = None
    codigo_municipio: int | None = None
    municipio: str | None = None
    estado: str | None = None
    codigo_orgao: int | None = None
    nome_orgao: str | None = None
    poder: str | None = None
    esfera: str | None = None
    data_compra: str | None = None
    data_hora_atualizacao_compra: str | None = None
    data_hora_atualizacao_item: str | None = None
    data_resultado: str | None = None
    data_hora_atualizacao_uasg: str | None = None
    objeto_compra: str | None = None
    descricao_detalhada_item: str | None = None
    data_atualizacao_fato: str | None = None

    @field_validator("id_compra", mode="before")
    @classmethod
    def id_compra_text(cls, value: object) -> str:
        return coerce_id_text(value, "id_compra")

    @field_validator(*_FLOAT_FIELDS, mode="before")
    @classmethod
    def optional_floats(cls, value: object) -> float | None:
        return coerce_optional_float(value)

    @field_validator(*_NAME_FIELDS)
    @classmethod
    def optional_names_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
