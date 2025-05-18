"""This module contains the configuration settings for the application."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """This class contains the configuration settings for the application."""

    FE_URLS: list[str] = Field(default_factory=list)
    ENVIRONMENT: Literal["local", "dev", "staging", "production"] = "local"
