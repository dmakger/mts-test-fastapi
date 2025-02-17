from sqlalchemy import Column, Integer, String

from .base import Base


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    level = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Level(id={self.id}, name={self.name}, level={self.level})>"
