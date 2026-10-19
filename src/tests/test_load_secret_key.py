import pytest
from pathlib import Path
import os
from config.load_secret_key import load_secret_key_func

@pytest.fixture(autouse=True)
def limpar_ambiente():
    """Garante que a variável de ambiente não vaze entre um teste e outro."""
    os.environ.pop("DADOS_GOV_API_KEY", None)
    yield
    os.environ.pop("DADOS_GOV_API_KEY", None)


def test_load_secret_key_func_sucesss(tmp_path: Path):
    """Devolve a chave quando o arquivo e a variável existem."""
    env_file = tmp_path / ".env"
    env_file.write_text("DADOS_GOV_API_KEY=minha_chave_secreta_123\n", encoding="utf-8")

    result = load_secret_key_func(env_file, "DADOS_GOV_API_KEY")
    assert result == "minha_chave_secreta_123"

def test_load_secret_key_func_file_not_found(tmp_path: Path):
    """Falha com FileNotFoundError quando o arquivo não existe."""
    env_file = tmp_path / ".env"
    with pytest.raises(FileNotFoundError):
        load_secret_key_func(env_file, "DADOS_GOV_API_KEY")

def test_absent_env_variable(tmp_path: Path):
    """Falha com KeyError quando a variável pedida não está no arquivo."""
    env_file = tmp_path / ".env"
    env_file.write_text("DADOS_GOV_API_KEY=minha_chave_secreta_123\n", encoding="utf-8")
    with pytest.raises(KeyError):
        load_secret_key_func(env_file, "DEEPSEEK_API_KEY") 

def test_absent_value_variable(tmp_path: Path):
    """Falha com ValueError quando o valor da variável está vazio."""
    env_file = tmp_path / ".env"
    env_file.write_text("DADOS_GOV_API_KEY=\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_secret_key_func(env_file, "DADOS_GOV_API_KEY")

def test_strip_spaces_on_the_borders(tmp_path: Path):
    """Remove espaços nas pontas do valor lido."""
    env_file = tmp_path / ".env"
    env_file.write_text("DADOS_GOV_API_KEY=' minha_chave '")

    result = load_secret_key_func(env_file, "DADOS_GOV_API_KEY")
    assert result == "minha_chave"

