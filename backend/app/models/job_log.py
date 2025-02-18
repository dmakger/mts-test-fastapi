from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import relationship

from . import Base


class JobLog(Base):
    __tablename__ = "job_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    column_name = Column(String(50), nullable=False)
    old_value = Column(String(100))
    new_value = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    job = relationship("Job", back_populates="logs")

    def __repr__(self):
        return f"<JobLog(id={self.id}, job_id={self.job_id}, column_name={self.column_name}, created_at={self.created_at})>"
