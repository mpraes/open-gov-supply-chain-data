from pydantic import BaseModel, ConfigDict, field_validator


class MaterialItemRecord(BaseModel):
    """Validated material item row mapped from consultarItemMaterial.

    Example:
        MaterialItemRecord(
            cod_item=9001,
            cod_grupo=10,
            nome_grupo="grupo",
            cod_classe=101,
            nome_classe="classe",
            cod_pdm=1001,
            nome_pdm="pdm",
            descricao_item="item",
            status_item=True,
            item_sustentavel=False,
            codigo_ncm="12345678",
            descricao_ncm="ncm",
            aplica_margem_preferencia=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_item: int
    cod_grupo: int
    nome_grupo: str
    cod_classe: int
    nome_classe: str
    cod_pdm: int
    nome_pdm: str
    descricao_item: str
    status_item: bool
    item_sustentavel: bool
    codigo_ncm: str | None
    descricao_ncm: str | None
    aplica_margem_preferencia: bool | None
    data_hora_atualizacao: str

    @field_validator("nome_grupo", "nome_classe", "nome_pdm", "descricao_item")
    @classmethod
    def text_must_be_upper_non_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("text fields must be non-empty")
        return cleaned.upper()

    @field_validator("descricao_ncm")
    @classmethod
    def descricao_ncm_upper(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().upper()

    @field_validator("codigo_ncm")
    @classmethod
    def codigo_ncm_strip(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()
