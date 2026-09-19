from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import upper_non_empty, upper_optional


class ServicoGrupoRecord(BaseModel):
    """Validated grupo row from consultarGrupoServico.

    Example:
        ServicoGrupoRecord(
            cod_grupo=3, cod_divisao=2, nome_secao="s", nome_divisao="d",
            nome_grupo="g", status_grupo=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )
    """

    model_config = ConfigDict(strict=True)

    cod_grupo: int
    cod_divisao: int
    # API docs show string, but real payloads sometimes send nomeSecao=null.
    nome_secao: str | None
    nome_divisao: str
    nome_grupo: str
    status_grupo: bool
    data_hora_atualizacao: str

    @field_validator("nome_secao")
    @classmethod
    def nome_secao_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)

    @field_validator("nome_divisao", "nome_grupo")
    @classmethod
    def nomes_upper(cls, value: str) -> str:
        return upper_non_empty(value, "nome")
