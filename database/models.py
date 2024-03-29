from sqlalchemy import Column, Integer, String, UniqueConstraint

from .database import Base


class GameOfLife(Base):
    __tablename__ = "game_of_life"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ecosystem = Column(String(255))
    evolutions = Column(Integer)
    messages = Column(Integer)

    __table_args__ = (UniqueConstraint("id"),)
