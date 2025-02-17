from sqlalchemy import Column, Integer, String

from .base import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Employee(id={self.id}, fio={self.fio})>"
