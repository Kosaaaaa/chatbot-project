"""This module contains the configuration settings for the application."""

from pathlib import Path
from typing import ClassVar, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent


class Settings(BaseSettings):
    """This class contains the configuration settings for the application."""

    FE_URLS: list[str] = Field(default_factory=list)
    ENVIRONMENT: Literal["local", "dev", "staging", "production"] = "local"

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    OPENAI_MODEL_NAME: str = "deepseek-r1:1.5b"
    OPENAI_PROVIDER_BASE_URL: str = "http://127.0.0.1:11434/v1"

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )
