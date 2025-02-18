from sqlalchemy import Column, Integer, ForeignKey, Date, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship

from . import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    employment_type_id = Column(Integer, ForeignKey("employment_types.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)
    division_id = Column(Integer, ForeignKey("divisions.id"), nullable=False)
    head_id = Column(Integer, ForeignKey("employees.id"))
    hire_date = Column(Date, nullable=False)
    dismissal_date = Column(Date)
    salary = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    employee = relationship("Employee", back_populates="jobs", foreign_keys=[employee_id])
    employment_type = relationship("EmploymentType", back_populates="jobs")
    position = relationship("Position", back_populates="jobs")
    division = relationship("Division", back_populates="jobs")
    head = relationship("Employee", back_populates="head_jobs", foreign_keys=[head_id])
    logs = relationship("JobLog", back_populates="job")

    def __repr__(self):
        return f"<Job(id={self.id}, employee_id={self.employee_id}, position_id={self.position_id}, salary={self.salary})>"
