from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"))
    name = Column(String(100), nullable=False)

    level = relationship("Level", back_populates="positions")
    jobs = relationship("Job", back_populates="position")

    def __repr__(self):
        return f"<Position(id={self.id}, name={self.name}, level_id={self.level_id})>"
