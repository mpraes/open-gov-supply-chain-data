from pydantic import BaseModel, ConfigDict, field_validator


class MaterialPdmRecord(BaseModel):
    """Validated material PDM row mapped from consultarPdmMaterial.

    Example:
        MaterialPdmRecord(
            cod_pdm=1001,
            cod_classe=101,
            cod_grupo=10,
            nome_grupo="grupo",
            nome_classe="classe",
            nome_pdm="pdm",
            status_pdm=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_pdm: int
    cod_classe: int
    cod_grupo: int
    nome_grupo: str
    nome_classe: str
    nome_pdm: str
    status_pdm: bool
    data_hora_atualizacao: str

    @field_validator("nome_grupo", "nome_classe", "nome_pdm")
    @classmethod
    def nome_must_be_upper(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("nome fields must be non-empty")
        return cleaned.upper()
