from pydantic import BaseModel, ConfigDict, field_validator

from contracts.coerce import coerce_id_text
from contracts.text_normalize import upper_optional


class PrecoDetalheRecord(BaseModel):
    """Validated detalhe row shared by material and serviço price APIs.

    Example:
        PrecoDetalheRecord(
            id_compra=1, id_item_compra=2, codigo_item_catalogo=3,
            objeto_compra="objeto", descricao_detalhada_item="detalhe",
            data_atualizacao_fato="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    id_compra: str
    id_item_compra: int
    numero_item_compra: int | None = None
    codigo_item_catalogo: int
    objeto_compra: str | None = None
    descricao_detalhada_item: str | None = None
    data_atualizacao_fato: str | None = None

    @field_validator("id_compra", mode="before")
    @classmethod
    def id_compra_text(cls, value: object) -> str:
        return coerce_id_text(value, "id_compra")

    @field_validator("objeto_compra", "descricao_detalhada_item")
    @classmethod
    def optional_text_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)


class PrecoMaterialDetalheRecord(PrecoDetalheRecord):
    """Detalhe row from consultarMaterialDetalhe."""


class PrecoServicoDetalheRecord(PrecoDetalheRecord):
    """Detalhe row from consultarServicoDetalhe."""
