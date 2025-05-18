from pathlib import Path

from app.config import PROJECT_DIR


def get_index_html_file_path() -> Path:
    return PROJECT_DIR / "application" / "static" / "index.html"
