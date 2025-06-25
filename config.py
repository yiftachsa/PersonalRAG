from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

import os

# Pydantic automatically:
# 1) Reads the .env file.
# 2) Loads environment variables into the Settings class.
# 3) Validates the types and required fields.
#
# Variable Priority Order (first match wins):
# 1) Environment variables from the system
# 2) Variables from the .env file
# 3) Default values in the class

# _ = load_dotenv(find_dotenv())
PROJECT_ROOT = Path(__file__).parent

class Settings(BaseSettings):
    # Required settings (no default, will raise error if not set)
    OPENAI_API_KEY: str
    HF_TOKEN: str

    # Application settings - Optional settings with defaults
    DEBUG: bool = False

    DEFAULT_VERSION: str = "1.0"
    DATA_DIR: str = str(PROJECT_ROOT / "data")

    # RAG & Models settings
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMP: float = 0
    SEARCH_TYPE: str = "mmr"
    CHAIN_TYPE: str = "stuff"

    COMPRESS_QUERY: bool = False
    LLM_MODEL_COMPRESS: str = "gpt-3.5-turbo-instruct"
    LLM_TEMP_COMPRESS: float = 0

    class Config:
        env_file = PROJECT_ROOT / ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True


# print(f"Project root: {PROJECT_ROOT}")
# print(f"Looking for .env at: {PROJECT_ROOT / '.env'}")
# print(f".env exists: {(PROJECT_ROOT / '.env').exists()}")

settings = Settings()
