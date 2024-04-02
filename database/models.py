from sqlalchemy import Column, Date, Integer, String, UniqueConstraint

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ecosystems_created = Column(Integer)
    ecosystems_killed = Column(Integer)
    ecosystems_evolved = Column(Integer)

    __table_args__ = (UniqueConstraint("id"),)


class Ecosystem(Base):
    __tablename__ = "ecosystems"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ecosystem = Column(String(255))
    evolutions = Column(Integer)
    messages = Column(Integer)
    born_date = Column(Date)
    extinction_date = Column(Date)

    __table_args__ = (UniqueConstraint("id"),)
