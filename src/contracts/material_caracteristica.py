from pydantic import BaseModel, ConfigDict, field_validator


class MaterialCaracteristicaRecord(BaseModel):
    """Validated item characteristic row from consultarMaterialCaracteristicas.

    Example:
        MaterialCaracteristicaRecord(
            cod_item=9001,
            item_sustentavel=True,
            status_item=True,
            codigo_caracteristica="c1",
            nome_caracteristica="cor",
            status_caracteristica=True,
            codigo_valor_caracteristica="v1",
            nome_valor_caracteristica="azul",
            status_valor_caracteristica=True,
            numero_caracteristica=1,
            sigla_unidade_medida="un",
            data_hora_atualizacao="2022-01-01T00:00:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_item: int
    item_sustentavel: bool | None
    status_item: bool | None
    codigo_caracteristica: str
    nome_caracteristica: str | None
    status_caracteristica: bool | None
    codigo_valor_caracteristica: str
    nome_valor_caracteristica: str | None
    status_valor_caracteristica: bool | None
    numero_caracteristica: int
    sigla_unidade_medida: str | None
    data_hora_atualizacao: str | None

    @field_validator("codigo_caracteristica", "codigo_valor_caracteristica")
    @classmethod
    def codigo_must_be_upper_non_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("codigo fields must be non-empty")
        return cleaned.upper()

    @field_validator("nome_caracteristica", "nome_valor_caracteristica", "sigla_unidade_medida")
    @classmethod
    def optional_text_upper(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("text fields must be non-empty when provided")
        return cleaned.upper()
