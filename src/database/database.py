from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.utils.config import Config

config = Config()

db_path = "sqlite:///src/database/game_of_life.db"

engine = create_engine(
    db_path,
    pool_size=20,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
