from datetime import date, datetime

from fastapi import UploadFile, HTTPException

from .models import LevelService
from ..services.models.employee import EmployeeService
from ..services.models.job import JobService
from ..services.models.division import DivisionService
from ..services.models.position import PositionService
from ..services.models.employment_type import EmploymentTypeService
from ..services.models.job_log import JobLogService
from ..utils.file_parser import parse_excel, OUTPUT_DATE_FORMAT
from ..core.database import SessionLocal


class FileService:
    async def process_file(self, file: UploadFile):
        if not file.filename.endswith(".xlsb"):
            raise HTTPException(status_code=400, detail="Файл должен быть в формате .xlsb")

        df, date_file, hash_data = await parse_excel(file)

        # Открываем сессию с БД
        async with SessionLocal() as session:
            employee_service = EmployeeService(session)
            job_service = JobService(session)
            division_service = DivisionService(session)
            position_service = PositionService(session)
            employment_type_service = EmploymentTypeService(session)
            job_log_service = JobLogService(session)
            default_levels = await LevelService(session).get_default_levels()
            department_level_id = default_levels.get("Департамент")
            division_level_id = default_levels.get("Отдел")

            for _, row in df.iterrows():
                await self._process_row(
                    row,
                    employee_service,
                    job_service,
                    division_service,
                    position_service,
                    employment_type_service,
                    job_log_service,
                    date_file,
                    department_level_id,
                    division_level_id,
                )

            await session.commit()

        processed_records = len(df)  # Пример подсчёта количества обработанных записей
        return {"message": "Файл успешно загружен и обработан", "processed_records": processed_records}

    async def _process_row(
            self, row,
            employee_service, job_service, division_service, position_service, employment_type_service, job_log_service,
            date_file, department_level_id, division_level_id
    ):
        """Обрабатывает одну строку из Excel-файла, обновляя `jobs` и `job_logs`"""

        head = await employee_service.get_or_create({"fio": row["head"]})
        employee = await employee_service.get_or_create({"fio": row["fio"]})
        employment_type = await employment_type_service.get_or_create({"name": row["employment_type"]})
        position = await position_service.get_or_create({"name": row["position"]})
        department = await division_service.get_or_create({"level_id": department_level_id, "name": row["department"]})
        division = await division_service.get_or_create(
            {"level_id": division_level_id, "parent_id": department.id, "name": row["division"]}
        )

        hire_date = datetime.strptime(row["hire_date"], OUTPUT_DATE_FORMAT).date()
        print("QWE123", row["hire_date"], hire_date)

        dismissal_date = row.get("dismissal_date")
        if dismissal_date and dismissal_date.strip():  # Проверяем, что значение не пустое
            dismissal_date = datetime.strptime(dismissal_date, OUTPUT_DATE_FORMAT).date()
        else:
            dismissal_date = None  # Если значение пустое, передаём None

        await job_service.create_smart({
            "employee_id": employee.id,
            "employment_type_id": employment_type.id,
            "position_id": position.id,
            "division_id": division.id,
            "head_id": head.id,
            "hire_date": hire_date,
            "dismissal_date": dismissal_date,
            "salary": row["salary"],
            "created_at": date_file,
        }, job_log_service)
