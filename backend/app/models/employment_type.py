from sqlalchemy import Column, Integer, String

from .base import Base


class EmploymentType(Base):
    __tablename__ = "employment_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<EmploymentType(id={self.id}, name={self.name})>"
