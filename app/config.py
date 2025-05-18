"""This module contains the configuration settings for the application."""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings

PROJECT_DIR = Path(__file__).parent


class Settings(BaseSettings):
    """This class contains the configuration settings for the application."""

    FE_URLS: list[str] = Field(default_factory=list)
    ENVIRONMENT: Literal["local", "dev", "staging", "production"] = "local"
