from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_non_empty


class ServicoDivisaoRecord(BaseModel):
    """Validated divisão row from consultarDivisaoServico.

    Example:
        ServicoDivisaoRecord(
            cod_divisao=2, cod_secao=1, nome_secao="s", nome_divisao="d",
            status_divisao=True, data_hora_atualizacao="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_divisao: int
    cod_secao: int
    nome_secao: str
    nome_divisao: str
    status_divisao: bool
    data_hora_atualizacao: str

    @field_validator("nome_secao", "nome_divisao")
    @classmethod
    def nomes_upper(cls, value: str) -> str:
        return upper_non_empty(value, "nome")
