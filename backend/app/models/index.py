from sqlalchemy import Index

from backend.app.models.job import Job
from backend.app.models.job_log import JobLog

Index("idx_jobs_employee_id", Job.employee_id)
Index("idx_jobs_position_id", Job.position_id)
Index("idx_jobs_division_id", Job.division_id)
Index("idx_jobs_salary", Job.salary)
Index("idx_job_logs_job_id", JobLog.job_id)
Index("idx_job_logs_created_at", JobLog.created_at)
