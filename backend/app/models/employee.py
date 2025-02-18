from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String(100), nullable=False)

    head_jobs = relationship("Job", back_populates="head", foreign_keys="[Job.head_id]")
    jobs = relationship("Job", back_populates="employee", foreign_keys="[Job.employee_id]")

    def __repr__(self):
        return f"<Employee(id={self.id}, fio={self.fio})>"
