from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...schemas import JobFilterSchema, JobSerializerResponse, JobResponse
from ...services.models import JobService, ResponseFormat, ReturnType

router = APIRouter()


# Создаем зависимость для JobService
def get_job_service(db: AsyncSession = Depends(get_db)) -> JobService:
    return JobService(db)


# Получаем список сотрудников
@router.get("/all", response_model=List[JobSerializerResponse | JobResponse])
async def get_jobs(
        filters: JobFilterSchema = Depends(),
        job_service: JobService = Depends(get_job_service)
):
    """
    Получение всех записей о работе из таблицы `jobs`
    """
    response_format = ResponseFormat.SERIALIZED if filters.model_dump(exclude_unset=True).get('serialize', False) else ResponseFormat.BASIC
    print("!!! API response_format", response_format)
    jobs_data = await job_service.find(filters, ReturnType.ALL, response_format=response_format)
    if not jobs_data:
        raise HTTPException(status_code=404, detail="No jobs found")
    return jobs_data
