from pydantic import BaseModel, ConfigDict, field_validator


class MaterialClassRecord(BaseModel):
    """Validated material class row mapped from consultarClasseMaterial.

    Example:
        MaterialClassRecord(
            cod_classe=101,
            cod_grupo=10,
            nome_grupo="grupo",
            nome_classe="classe",
            status_classe=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_classe: int
    cod_grupo: int
    nome_grupo: str
    nome_classe: str
    status_classe: bool
    data_hora_atualizacao: str

    @field_validator("nome_grupo", "nome_classe")
    @classmethod
    def nome_must_be_upper(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("nome fields must be non-empty")
        return cleaned.upper()
