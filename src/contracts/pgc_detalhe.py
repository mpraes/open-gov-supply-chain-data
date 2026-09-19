from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from contracts.coerce import coerce_id_text, coerce_optional_float
from contracts.text_normalize import upper_optional

_FLOAT_FIELDS = (
    "quantidade_item",
    "valor_unitario_item",
    "valor_total_item",
)

_ID_FIELDS = ("codigo_uasg", "orgao", "codigo_item_catalogo")

_NAME_FIELDS = (
    "nome_uasg",
    "descricao_artefato",
    "descricao_objeto_dfd",
    "codigo_area_dfd",
    "tipo_item",
    "nome_grupo_material",
    "nome_classe_material",
    "nome_pdm_material",
    "nome_secao_servico",
    "nome_divisao_servico",
    "nome_grupo_servico",
    "nome_classe_servico",
    "nome_subclasse_servico",
    "descricao_item_catalogo",
    "sigla_unidade_fornecimento",
    "nome_unidade_fornecimento",
    "titulo_projeto_compra",
    "descricao_projeto_compra",
)


class PgcDetalheRecord(BaseModel):
    """Validated PGC detalhe row from consultarPgcDetalhe.

    Example:
        PgcDetalheRecord(
            codigo_uasg="153001", orgao="36000", numero_artefato=1,
            ano_artefato=2026, ordem_dfd=0, codigo_item_catalogo="449156",
            ano_pca_projeto_compra=2026,
        )
    """

    model_config = ConfigDict(strict=True)

    codigo_uasg: str
    nome_uasg: str | None = None
    orgao: str
    numero_artefato: int
    ano_artefato: int
    codigo_estado_artefato: int | None = None
    codigo_categoria_artefato: int | None = None
    descricao_artefato: str | None = None
    codigo_tipo_artefato: int | None = None
    ordem_dfd: int
    descricao_objeto_dfd: str | None = None
    nivel_prioridade_dfd: int | None = None
    data_prevista_formalizacao_demanda: str | None = None
    codigo_area_dfd: str | None = None
    tipo_item: str | None = None
    item_sustentavel: bool | None = None
    codigo_grupo_material: int | None = None
    nome_grupo_material: str | None = None
    codigo_classe_material: int | None = None
    nome_classe_material: str | None = None
    codigo_pdm_material: int | None = None
    nome_pdm_material: str | None = None
    codigo_secao_servico: int | None = None
    nome_secao_servico: str | None = None
    codigo_divisao_servico: int | None = None
    nome_divisao_servico: str | None = None
    codigo_grupo_servico: int | None = None
    nome_grupo_servico: str | None = None
    codigo_classe_servico: int | None = None
    nome_classe_servico: str | None = None
    codigo_subclasse_servico: int | None = None
    nome_subclasse_servico: str | None = None
    codigo_item_catalogo: str
    descricao_item_catalogo: str | None = None
    sigla_unidade_fornecimento: str | None = None
    nome_unidade_fornecimento: str | None = None
    quantidade_item: float | None = None
    valor_unitario_item: float | None = None
    valor_total_item: float | None = None
    titulo_projeto_compra: str | None = None
    descricao_projeto_compra: str | None = None
    ano_pca_projeto_compra: int
    data_inicio_processo_compra: str | None = None
    data_fim_processo_compra: str | None = None
    duracao_processo_compra: int | None = None
    numero_item_pncp: int | None = None
    status_contratacao_execucao: int | None = None
    data_hora_publicacao_pncp: str | None = None
    data_hora_atualizacao_artefato: str | None = None
    data_hora_atualizacao_projeto_compra: str | None = None
    data_hora_atualizacao_dfd: str | None = None
    data_hora_atualizacao_item: str | None = None

    @field_validator(*_ID_FIELDS, mode="before")
    @classmethod
    def identity_text(cls, value: object, info: ValidationInfo) -> str:
        return coerce_id_text(value, info.field_name)

    @field_validator(*_FLOAT_FIELDS, mode="before")
    @classmethod
    def optional_floats(cls, value: object) -> float | None:
        return coerce_optional_float(value)

    @field_validator(*_NAME_FIELDS)
    @classmethod
    def optional_names_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
