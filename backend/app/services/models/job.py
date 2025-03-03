from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService, ReturnType, EmployeeService, EmploymentTypeService, PositionService, DivisionService
from ...models import Job
from ...schemas import JobBaseResponse, JobResponse, JobSerializerResponse, EmployeeResponse, EmploymentTypeResponse, \
    PositionSerializerResponse, DivisionSerializerResponse


class JobService(BaseService):
    # Указываем список отношений, которые нужно догружать при serialize=True
    relationships = [
        Job.employee,
        Job.employment_type,
        Job.position,
        Job.division,
        Job.head
    ]

    def __init__(self, session: AsyncSession):
        super().__init__(session, Job)
        self.employee_service = EmployeeService(session)
        self.employment_type_service = EmploymentTypeService(session)
        self.position_service = PositionService(session)
        self.division_service = DivisionService(session)

    # ========={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }=========
    def _to_base_response(self, item) -> JobBaseResponse:
        return JobBaseResponse.model_validate(item)

    def _to_basic_response(self, item) -> JobResponse:
        base_response = self._to_base_response(item)
        return JobResponse(
            **base_response.model_dump(),
            employee_id=item.employee_id,
            employment_type_id=item.employment_type_id,
            position_id=item.position_id,
            division_id=item.division_id,
            head_id=item.head_id
        )

    def _to_serialized_response(self, item) -> JobSerializerResponse:
        base_response = self._to_base_response(item)
        print("JOB _to_serialized_response", item)
        return JobSerializerResponse(
            **base_response.model_dump(),
            employee=self.employee_service._to_serialized_response(item.employee),
            employment_type=self.employment_type_service._to_serialized_response(item.employment_type),
            position=self.position_service._to_serialized_response(item.position),
            division=self.division_service._to_serialized_response(item.division),
            head=self.employee_service._to_serialized_response(item.head),
        )

    # ========={ ОБЩИЕ }=========

    async def create_smart(self, defaults: dict, job_log_service):
        """
        Создаёт или обновляет запись в таблицах `jobs` и `job_logs`.
        """
        immutable_fields = {
            "employee_id": defaults["employee_id"],
            "employment_type_id": defaults["employment_type_id"],
            "position_id": defaults["position_id"],
            "division_id": defaults["division_id"],
            "hire_date": defaults["hire_date"]
        }

        existing_job = await self.find(immutable_fields, return_type=ReturnType.FIRST)

        if existing_job:
            updates = {}
            logs = []

            old_dismissal_date = existing_job.dismissal_date
            new_dismissal_date = defaults.get("dismissal_date")

            fields_to_check = {
                "salary": defaults["salary"],
                "head_id": defaults["head_id"],
            }

            for field, new_value in fields_to_check.items():
                old_value = getattr(existing_job, field, None)
                if old_value != new_value:
                    updates[field] = new_value
                    log_created_at = defaults[
                        "created_at"] if old_dismissal_date and not new_dismissal_date else new_dismissal_date
                    logs.append({
                        "job_id": existing_job.id,
                        "column_name": field,
                        "old_value": str(old_value) if old_value else None,
                        "new_value": str(new_value),
                        "created_at": log_created_at
                    })

            if updates:
                await self.update(existing_job.id, updates)
                for log in logs:
                    await job_log_service.get_or_create(log, **log)
        else:
            await self.get_or_create(defaults, **defaults)
