from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings
from ..models.base import Base

engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


# Создание всех таблиц
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
