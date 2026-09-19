from pydantic import BaseModel, ConfigDict, field_validator

from contracts.text_normalize import strip_optional, upper_non_empty, upper_optional

_NAME_FIELDS = (
    "nome_mnemonico_orgao",
    "nome_orgao_vinculado",
    "nome_orgao_superior",
    "nome_tipo_administracao",
    "poder",
    "esfera",
)

_CODE_FIELDS = (
    "cnpj_cpf_orgao",
    "cnpj_cpf_orgao_vinculado",
    "cnpj_cpf_orgao_superior",
)


class UasgOrgaoRecord(BaseModel):
    """Validated órgão row from consultarOrgao.

    Example:
        UasgOrgaoRecord(codigo_orgao=36000, nome_orgao="mp", status_orgao=True)
    """

    model_config = ConfigDict(strict=True)

    codigo_orgao: int
    nome_orgao: str
    nome_mnemonico_orgao: str | None = None
    cnpj_cpf_orgao: str | None = None
    codigo_orgao_vinculado: int | None = None
    cnpj_cpf_orgao_vinculado: str | None = None
    nome_orgao_vinculado: str | None = None
    codigo_orgao_superior: int | None = None
    cnpj_cpf_orgao_superior: str | None = None
    nome_orgao_superior: str | None = None
    codigo_tipo_administracao: int | None = None
    nome_tipo_administracao: str | None = None
    poder: str | None = None
    esfera: str | None = None
    uso_sisg: bool | None = None
    status_orgao: bool
    data_hora_movimento: str | None = None

    @field_validator("nome_orgao")
    @classmethod
    def nome_upper(cls, value: str) -> str:
        return upper_non_empty(value, "nome_orgao")

    @field_validator(*_NAME_FIELDS)
    @classmethod
    def optional_names_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)

    @field_validator(*_CODE_FIELDS)
    @classmethod
    def optional_codes_strip(cls, value: str | None) -> str | None:
        return strip_optional(value)
