from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.employee import Employee


class EmployeeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, fio: str):
        """Ищет сотрудника или создает нового"""
        stmt = select(Employee).where(Employee.fio == fio)
        result = await self.session.execute(stmt)
        employee = result.scalars().first()

        if not employee:
            employee = Employee(fio=fio)
            self.session.add(employee)
            await self.session.commit()
            await self.session.refresh(employee)

        return employee
