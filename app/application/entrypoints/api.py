from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.entrypoints.chat import chat_router
from app.application.entrypoints.index import index_router
from app.application.entrypoints.introspections import introspections_router
from app.config import Settings
from app.infrastructure.database.base import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()

    yield


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.FE_URLS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(index_router)
    app.include_router(introspections_router)
    app.include_router(chat_router)

    return app
