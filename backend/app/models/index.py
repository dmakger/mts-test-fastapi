from sqlalchemy import Index

from . import Job
from . import JobLog

Index("idx_jobs_employee_id", Job.employee_id)
Index("idx_jobs_position_id", Job.position_id)
Index("idx_jobs_division_id", Job.division_id)
Index("idx_jobs_salary", Job.salary)
Index("idx_job_logs_job_id", JobLog.job_id)
Index("idx_job_logs_created_at", JobLog.created_at)
