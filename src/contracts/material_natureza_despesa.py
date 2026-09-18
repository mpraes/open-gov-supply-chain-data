from pydantic import BaseModel, ConfigDict, field_validator


class MaterialNaturezaDespesaRecord(BaseModel):
    """Validated PDM expense-nature row from consultarMaterialNaturezaDespesa.

    Example:
        MaterialNaturezaDespesaRecord(
            cod_pdm=1001,
            cod_natureza_despesa="339030",
            nome_natureza_despesa="material de consumo",
            status_natureza_despesa="ativo",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_pdm: int
    cod_natureza_despesa: str
    nome_natureza_despesa: str
    status_natureza_despesa: str | None

    @field_validator("cod_natureza_despesa")
    @classmethod
    def codigo_must_be_non_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("cod_natureza_despesa must be non-empty")
        return cleaned

    @field_validator("nome_natureza_despesa")
    @classmethod
    def nome_must_be_upper(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("nome_natureza_despesa must be non-empty")
        return cleaned.upper()

    @field_validator("status_natureza_despesa")
    @classmethod
    def status_upper_optional(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().upper()
