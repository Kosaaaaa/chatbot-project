from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.application.entrypoints.dependencies.static import get_chat_app_ts_file_path, get_index_html_file_path

index_router = APIRouter(include_in_schema=False)


@index_router.get("/")
async def index(index_html: Annotated[Path, Depends(get_index_html_file_path)]) -> FileResponse:
    return FileResponse(index_html, media_type="text/html")


@index_router.get("/chat_app.ts")
async def main_ts(chat_app_ts: Annotated[Path, Depends(get_chat_app_ts_file_path)]) -> FileResponse:
    return FileResponse(chat_app_ts, media_type="text/plain")
