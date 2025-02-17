from fastapi import UploadFile, HTTPException
from ..services.employee import EmployeeService
from ..services.job import JobService
from ..services.division import DivisionService
from ..services.position import PositionService
from ..services.employment_type import EmploymentTypeService
from ..utils.file_parser import parse_xlsb
from ..core.database import SessionLocal


class FileService:
    async def process_file(self, file: UploadFile):
        if not file.filename.endswith(".xlsb"):
            raise HTTPException(status_code=400, detail="Файл должен быть в формате .xlsb")

        df = await parse_xlsb(file)

        # Открываем сессию с БД
        async with SessionLocal() as session:
            employee_service = EmployeeService(session)
            job_service = JobService(session)
            division_service = DivisionService(session)
            position_service = PositionService(session)
            employment_type_service = EmploymentTypeService(session)

            for _, row in df.iterrows():
                await self._process_row(
                    row,
                    employee_service,
                    job_service,
                    division_service,
                    position_service,
                    employment_type_service
                )

            await session.commit()

        return {"message": "Файл успешно загружен и обработан"}

    async def _process_row(self, row, employee_service, job_service, division_service, position_service, employment_type_service):
        """Обрабатывает одну строку из Excel-файла"""
        employee = await employee_service.get_or_create(row["fio"])
        employment_type = await employment_type_service.get_or_create(row["employment_type"])
        position = await position_service.get_or_create(level_id=row["level_id"], name=row["position"])
        division = await division_service.get_or_create(
            level_id=row["level_id"],
            parent_id=row["parent_id"],
            name=row["division"]
        )

        # TODO: Добавить: авто-изменение job и заполнение job_log

        await job_service.get_or_create(
            employee_id=employee.id,
            employment_type_id=employment_type.id,
            position_id=position.id,
            division_id=division.id,
            hire_date=row["hire_date"],
            dismissal_date=row.get("dismissal_date"),
            salary=row["salary"]
        )
