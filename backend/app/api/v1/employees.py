from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...schemas import EmployeeFilterSchema, EmployeeResponse
from ...services.models import EmployeeService

router = APIRouter()


# Создаем зависимость для EmployeeService
def get_employee_service(db: AsyncSession = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


# Получаем список сотрудников
@router.get("/all", response_model=List[EmployeeResponse])
async def get_employees(
        filters: EmployeeFilterSchema = Depends(),
        employee_service: EmployeeService = Depends(get_employee_service)
):
    """
    Получение всех сотрудников из таблицы `employees`
    """
    employees_data = await employee_service.find(filters)
    if not employees_data:
        raise HTTPException(status_code=404, detail="No employees found")
    return employees_data
