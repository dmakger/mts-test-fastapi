from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    name = Column(String(100), nullable=False)

    level = relationship("Level", back_populates="positions")

    def __repr__(self):
        return f"<Position(id={self.id}, name={self.name}, level_id={self.level_id})>"
