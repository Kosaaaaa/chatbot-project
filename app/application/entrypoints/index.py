from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.application.entrypoints.dependencies.static import get_index_html_file_path

index_router = APIRouter()


@index_router.get("/")
async def index(index_html: Annotated[Path, Depends(get_index_html_file_path)]) -> FileResponse:
    return FileResponse(index_html, media_type="text/html")
