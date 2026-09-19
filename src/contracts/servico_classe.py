from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_non_empty


class ServicoClasseRecord(BaseModel):
    """Validated classe row from consultarClasseServico.

    Example:
        ServicoClasseRecord(
            cod_classe=4, cod_grupo=3, nome_grupo="g", nome_classe="c",
            status_classe=True, data_hora_atualizacao="2024-01-15T10:30:00",
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
    def nomes_upper(cls, value: str) -> str:
        return upper_non_empty(value, "nome")
