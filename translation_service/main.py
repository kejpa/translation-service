from pathlib import Path
import tomllib

from fastapi import FastAPI
from translation_service.database import create_tables
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
from translation_service.database import get_db
from translation_service.models import TranslationUnit

VERSION = Path("VERSION").read_text(encoding="utf-8").strip()

with open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

PROJECT_NAME = pyproject["project"]["name"]
PROJECT_DESCRIPTION = pyproject["project"].get("description", "")

create_tables()

app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=VERSION,
)


@app.get("/")
def root():
    return {"service": PROJECT_NAME, "version": VERSION, "status": "running"}


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "running",
        "database": "connected",
    }


@app.get("/translation-units")
def get_translation_units(
    db: Session = Depends(get_db),
):
    units = db.query(TranslationUnit).all()

    return [
        {
            "id": unit.id,
            "source_text": unit.source_text,
            "target_text": unit.target_text,
        }
        for unit in units
    ]
