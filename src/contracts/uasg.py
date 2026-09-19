from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from contracts.coerce import coerce_id_text
from contracts.text_normalize import strip_optional, upper_non_empty, upper_optional

_NAME_FIELDS = (
    "sigla_uf",
    "nome_municipio_ibge",
    "nome_unidade_polo",
    "nome_unidade_espelho",
)

_CODE_FIELDS = (
    "cnpj_cpf_uasg",
    "cnpj_cpf_orgao",
    "cnpj_cpf_orgao_vinculado",
    "cnpj_cpf_orgao_superior",
    "codigo_siorg",
)


class UasgRecord(BaseModel):
    """Validated UASG row from consultarUasg.

    Example:
        UasgRecord(codigo_uasg="153001", nome_uasg="uasg", status_uasg=True)
    """

    model_config = ConfigDict(strict=True)

    codigo_uasg: str
    nome_uasg: str
    uso_sisg: bool | None = None
    adesao_siasg: bool | None = None
    sigla_uf: str | None = None
    codigo_municipio: int | None = None
    codigo_municipio_ibge: int | None = None
    nome_municipio_ibge: str | None = None
    codigo_unidade_polo: int | None = None
    nome_unidade_polo: str | None = None
    codigo_unidade_espelho: int | None = None
    nome_unidade_espelho: str | None = None
    uasg_cadastradora: bool | None = None
    cnpj_cpf_uasg: str | None = None
    codigo_orgao: int | None = None
    cnpj_cpf_orgao: str | None = None
    cnpj_cpf_orgao_vinculado: str | None = None
    cnpj_cpf_orgao_superior: str | None = None
    codigo_siorg: str | None = None
    status_uasg: bool
    data_implantacao_sidec: str | None = None
    data_hora_movimento: str | None = None

    @field_validator("codigo_uasg", mode="before")
    @classmethod
    def identity_text(cls, value: object, info: ValidationInfo) -> str:
        return coerce_id_text(value, info.field_name)

    @field_validator("nome_uasg")
    @classmethod
    def nome_upper(cls, value: str) -> str:
        return upper_non_empty(value, "nome_uasg")

    @field_validator(*_NAME_FIELDS)
    @classmethod
    def optional_names_upper(cls, value: str | None) -> str | None:
        return upper_optional(value)

    @field_validator(*_CODE_FIELDS)
    @classmethod
    def optional_codes_strip(cls, value: str | None) -> str | None:
        return strip_optional(value)
