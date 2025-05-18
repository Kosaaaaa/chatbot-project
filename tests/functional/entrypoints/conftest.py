# pyright: reportPrivateUsage=false, reportUnusedCallResult=false
from __future__ import annotations

from collections.abc import AsyncGenerator

import httpx
import pytest
from fastapi import FastAPI
from polyfactory.factories.pydantic_factory import ModelFactory

from app.application.entrypoints.api import create_app
from app.config import Settings
from app.dependencies import get_settings


@pytest.fixture
def test_app(
    settings_factory: ModelFactory[Settings],
) -> FastAPI:
    settings = settings_factory.build()

    app = create_app(settings=settings)

    app.dependency_overrides[get_settings] = lambda: settings

    return app


@pytest.fixture
async def test_client(test_app: FastAPI) -> AsyncGenerator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=test_app),  # type: ignore
        base_url="http://testserver",
    ) as async_client:
        yield async_client
