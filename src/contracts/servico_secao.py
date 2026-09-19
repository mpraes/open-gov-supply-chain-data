from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_non_empty


class ServicoSecaoRecord(BaseModel):
    """Validated seção row from consultarSecaoServico.

    Example:
        ServicoSecaoRecord(
            cod_secao=1, nome_secao="secao", status_secao=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_secao: int
    nome_secao: str
    status_secao: bool
    data_hora_atualizacao: str

    @field_validator("nome_secao")
    @classmethod
    def nome_upper(cls, value: str) -> str:
        return upper_non_empty(value, "nome_secao")
