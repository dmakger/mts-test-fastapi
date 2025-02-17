from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# from .api.v1 import employees, divisions, jobs, files
from .api.v1 import files
from .utils.logger import logger


app = FastAPI(title="HR Management API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
# app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
# app.include_router(divisions.router, prefix="/api/v1/divisions", tags=["Divisions"])
# app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(files.router, prefix="/api/v1/files", tags=["Files"])

@app.on_event("startup")
async def startup():
    logger.info("API запущен")

@app.get("/")
async def root():
    return {"message": "HR Management API is running!"}
