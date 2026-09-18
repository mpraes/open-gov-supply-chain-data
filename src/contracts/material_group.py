from pydantic import BaseModel, field_validator, ConfigDict

class MaterialGroupRecord(BaseModel):
      model_config = ConfigDict(strict=True)  # no bool→int coercion
      cod_grupo: int
      nome_grupo: str
      status_grupo: bool
      data_hora_atualizacao: str  # or datetime if you parse it
      @field_validator("nome_grupo")
      @classmethod
      def nome_must_be_upper(cls, value: str) -> str:
          cleaned = value.strip()
          if not cleaned:
              raise ValueError("nome_grupo must be non-empty")
          return cleaned.upper()