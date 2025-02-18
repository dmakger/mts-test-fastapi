from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Division(Base):
    __tablename__ = "divisions"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("divisions.id"))
    name = Column(String(100), nullable=False)

    parent = relationship("Division", remote_side=[id], back_populates="children")
    children = relationship("Division", back_populates="parent")
    level = relationship("Level", back_populates="divisions")
    jobs = relationship("Job", back_populates="division")

    def __repr__(self):
        return f"<Division(id={self.id}, name={self.name}, level_id={self.level_id})>"
