from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.dependencies import get_settings

_SETTINGS = get_settings()

DATABASE_URL = f"postgresql+asyncpg://{_SETTINGS.DB_USER}:{_SETTINGS.DB_PASSWORD}@{_SETTINGS.DB_HOST}:{_SETTINGS.DB_PORT}/{_SETTINGS.DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
