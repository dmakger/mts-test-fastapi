from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class EmploymentType(Base):
    __tablename__ = "employment_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    jobs = relationship("Job", back_populates="employment_type")

    def __repr__(self):
        return f"<EmploymentType(id={self.id}, name={self.name})>"
