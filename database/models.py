from sqlalchemy import Column, Integer, String, UniqueConstraint

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ecosystems_created = Column(Integer)
    ecosystems_killed = Column(Integer)
    ecosystems_evolved = Column(Integer)

    __table_args__ = (UniqueConstraint("id"),)


class GameOfLife(Base):
    __tablename__ = "game_of_life"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ecosystem = Column(String(255))
    evolutions = Column(Integer)
    messages = Column(Integer)

    __table_args__ = (UniqueConstraint("id"),)
