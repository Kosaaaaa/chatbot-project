from typing import Annotated

from fastapi import Depends
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from app.config import Settings
from app.dependencies import get_settings


def get_openai_model(settings: Annotated[Settings, Depends(get_settings)]) -> OpenAIModel:
    return OpenAIModel(
        model_name=settings.OPENAI_MODEL_NAME,
        provider=OpenAIProvider(base_url=settings.OPENAI_PROVIDER_BASE_URL),
    )


def get_agent(openai_model: Annotated[OpenAIModel, Depends(get_openai_model)]) -> Agent:
    return Agent(model=openai_model)
