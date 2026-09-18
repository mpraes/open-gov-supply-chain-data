from pydantic import BaseModel, ConfigDict, field_validator


class MaterialUnidadeFornecimentoRecord(BaseModel):
    """Validated supply-unit row from consultarMaterialUnidadeFornecimento.

    Example:
        MaterialUnidadeFornecimentoRecord(
            cod_pdm=1001,
            sigla_unidade_fornecimento="un",
            nome_unidade_fornecimento="unidade",
            descricao_unidade_fornecimento="unidade de fornecimento",
            sigla_unidade_medida="un",
            capacidade_unidade_fornecimento=1,
            numero_sequencial_unidade_fornecimento=1,
            status_unidade_fornecimento_pdm=True,
            status_unidade_fornecimento=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_pdm: int
    sigla_unidade_fornecimento: str
    nome_unidade_fornecimento: str | None
    descricao_unidade_fornecimento: str | None
    sigla_unidade_medida: str | None
    capacidade_unidade_fornecimento: float | None
    numero_sequencial_unidade_fornecimento: int
    status_unidade_fornecimento_pdm: bool | None
    status_unidade_fornecimento: bool | None
    data_hora_atualizacao: str | None

    @field_validator("capacidade_unidade_fornecimento", mode="before")
    @classmethod
    def capacidade_as_float(cls, value: object) -> float | None:
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                f"capacidade_unidade_fornecimento must be a number or null, got {value!r}"
            )
        return float(value)

    @field_validator("sigla_unidade_fornecimento")
    @classmethod
    def sigla_must_be_upper_non_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("sigla_unidade_fornecimento must be non-empty")
        return cleaned.upper()

    @field_validator(
        "nome_unidade_fornecimento",
        "descricao_unidade_fornecimento",
        "sigla_unidade_medida",
    )
    @classmethod
    def optional_text_upper(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        return cleaned.upper()
