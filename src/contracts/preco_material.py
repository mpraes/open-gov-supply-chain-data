from pydantic import field_validator

from contracts.coerce import coerce_optional_float
from contracts.preco_servico import PrecoServicoRecord
from contracts.text_normalize import upper_optional

_MATERIAL_FLOAT_FIELDS = ("capacidade_unidade_fornecimento",)
_MATERIAL_NAME_FIELDS = (
    "sigla_unidade_fornecimento",
    "nome_unidade_fornecimento",
    "marca",
    "nome_classe",
    "id_compra_item",
    "codigo_pdm",
    "nome_pdm",
)


class PrecoMaterialRecord(PrecoServicoRecord):
    """Validated price row from consultarMaterial, including CATMAT extras.

    Example:
        PrecoMaterialRecord(
            id_compra=99, id_item_compra=1, codigo_item_catalogo=123,
            descricao_item="notebook", preco_unitario=10,
        )
    """

    sigla_unidade_fornecimento: str | None = None
    nome_unidade_fornecimento: str | None = None
    capacidade_unidade_fornecimento: float | None = None
    marca: str | None = None
    codigo_classe: int | None = None
    nome_classe: str | None = None
    id_compra_item: str | None = None
    codigo_pdm: str | None = None
    nome_pdm: str | None = None

    @field_validator(*_MATERIAL_FLOAT_FIELDS, mode="before")
    @classmethod
    def material_optional_floats(cls, value: object) -> float | None:
        return coerce_optional_float(value)

    @field_validator(*_MATERIAL_NAME_FIELDS)
    @classmethod
    def material_optional_names_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)
