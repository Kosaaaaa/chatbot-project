from app.application.entrypoints.api import create_app
from app.dependencies import get_settings

_SETTINGS = get_settings()

app = create_app(settings=_SETTINGS)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None, log_level=None)
