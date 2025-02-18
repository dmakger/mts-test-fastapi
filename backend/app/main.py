from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.v1 import files, employees
from .core.database import SessionLocal
from .services.models import LevelService
from .utils.logger import logger

app = FastAPI(title="HR Management API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(files.router, prefix="/api/v1/files", tags=["Files"])
app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])


@app.on_event("startup")
async def startup():
    async with SessionLocal() as session:
        level_service = LevelService(session)
        await level_service.initialize_levels()
    logger.info("API запущен")


@app.get("/")
async def root():
    return {"message": "HR Management API is running!"}
