"""Contrato da linha de seção de consultarSecaoServico."""

from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_non_empty


class ServicoSecaoRecord(BaseModel):
    """Linha validada de seção de consultarSecaoServico.

    Exemplo:
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
        """Rejeita nome_secao vazio e devolve o texto em maiúsculas."""
        return upper_non_empty(value, "nome_secao")
