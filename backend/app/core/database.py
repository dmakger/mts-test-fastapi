from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from ..models.base import Base


engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, class_=AsyncSession, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создание всех таблиц
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

