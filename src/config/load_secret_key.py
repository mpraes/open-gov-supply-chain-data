import os
from pathlib import Path
from dotenv import load_dotenv

def load_secret_key_func(env_path: str | Path, env_name: str) -> str:
    path = Path(env_path)

    #Error file not found
    if not path.is_file():
        raise FileNotFoundError(f"Env file not found: {path}")

    # Loading variable file, no override
    load_dotenv(dotenv_path=path, override=False)

    if env_name not in os.environ:
        raise KeyError (f"Variable {env_name} not found on the file")

    secret_key = os.getenv(env_name)

    #Validating the value
    if not secret_key or not secret_key.strip():
        raise ValueError("Key {env_name} is defined, but no valid value inside")

    return secret_key.strip()

# if __name__ == "__main__":
    # secret_key = load_secret_key_func("/home/renan/personal/projects/open-gov-supply-chain-data/.env", "DEEPSEEK_API_KEY")
    # print(secret_key)