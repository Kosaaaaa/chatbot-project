from app.application.entrypoints.dependencies.static import get_index_html_file_path


def test_get_index_html_file_path() -> None:
    result = get_index_html_file_path()

    assert result.exists()


def test_get_chat_app_ts_file_path() -> None:
    result = get_index_html_file_path()

    assert result.exists()
