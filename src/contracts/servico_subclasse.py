from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_non_empty


class ServicoSubclasseRecord(BaseModel):
    """Validated subclasse row from consultarSubClasseServico.

    Example:
        ServicoSubclasseRecord(
            cod_subclasse=5, cod_classe=4, nome_classe="c", nome_subclasse="sc",
            status_subclasse=True, data_hora_atualizacao="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_subclasse: int
    cod_classe: int
    nome_classe: str
    nome_subclasse: str
    status_subclasse: bool
    data_hora_atualizacao: str

    @field_validator("nome_classe", "nome_subclasse")
    @classmethod
    def nomes_upper(cls, value: str) -> str:
        return upper_non_empty(value, "nome")
