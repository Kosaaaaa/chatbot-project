from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.entrypoints.introspections import introspections_router
from app.config import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.FE_URLS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(introspections_router)

    return app
