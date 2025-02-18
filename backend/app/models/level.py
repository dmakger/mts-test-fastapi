from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    level = Column(Integer, nullable=False, default=1)

    divisions = relationship("Division", back_populates="level")
    positions = relationship("Position", back_populates="level")

    def __repr__(self):
        return f"<Level(id={self.id}, name={self.name}, level={self.level})>"




