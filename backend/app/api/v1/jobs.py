from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...schemas import JobFilterSchema, JobSerializerResponse
from ...services.models import JobService

router = APIRouter()


# Создаем зависимость для JobService
def get_job_service(db: AsyncSession = Depends(get_db)) -> JobService:
    return JobService(db)


# Получаем список сотрудников
@router.get("/all", response_model=List[JobSerializerResponse])
async def get_jobs(
        filters: JobFilterSchema = Depends(),
        job_service: JobService = Depends(get_job_service)
):
    """
    Получение всех записей о работе из таблицы `jobs`
    """
    jobs_data = await job_service.find(filters)
    print("QWE", jobs_data)
    if not jobs_data:
        raise HTTPException(status_code=404, detail="No jobs found")
    return jobs_data
