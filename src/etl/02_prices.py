import os
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://dadosabertos.compras.gov.br"
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def load_dados_gov_api_key(env_path: Path = ENV_PATH) -> str:
    """Load DADOS_GOV_API_KEY from .env, then the process environment.

    Example:
        api_key = load_dados_gov_api_key()
    """
    for line in _read_env_lines(env_path):
        name, _, value = line.partition("=")
        if name.strip() == "DADOS_GOV_API_KEY" and value.strip():
            return value.strip()
    env_key = os.getenv("DADOS_GOV_API_KEY")
    if env_key:
        return env_key
    raise ValueError(
        f"DADOS_GOV_API_KEY not found in {env_path} or environment; "
        "expected DADOS_GOV_API_KEY=<JWT>"
    )


def _read_env_lines(env_path: Path) -> list[str]:
    if not env_path.exists():
        return []
    return [
        line.strip()
        for line in env_path.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


# Exemplo: Consultar preços de um item específico (código do catálogo)
def fetch_preco_material(
    codigo_item: int,
    api_key: str,
    pagina: int = 1,
    tamanho_pagina: int = 100,
) -> dict:
    endpoint = f"{BASE_URL}/modulo-pesquisa-preco/1_consultarMaterial"
    params = {
        "tipo": "codigoItemCatalogo",
        "codigo": codigo_item,
        "pagina": pagina,
        "tamanhoPagina": tamanho_pagina,
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(endpoint, params=params, headers=headers)
    return response.json()


# Exemplo: Item "NOTEBOOK" (você precisa descobrir o código no CATMAT)
# Vamos chutar um código ou buscar no CATMAT primeiro
api_key = load_dados_gov_api_key()
data = fetch_preco_material(codigo_item=12345, api_key=api_key)  # Substitua pelo código real
print(f"Total de registros: {data.get('totalRegistros', 0)}")
print(f"Total de páginas: {data.get('totalPaginas', 0)}")

# Explorar a estrutura dos dados
if data.get("resultado"):
    print("\nEstrutura do primeiro registro:")
    print(pd.json_normalize(data["resultado"][0]).columns.tolist())
