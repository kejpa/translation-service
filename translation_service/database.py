import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from translation_service.models import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///translation_memory.db",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
