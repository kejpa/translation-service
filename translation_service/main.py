from pathlib import Path
import tomllib

from fastapi import FastAPI, File, HTTPException, UploadFile, Depends
from translation_service.database import get_db, create_tables
from sqlalchemy import text
from sqlalchemy.orm import Session

from translation_service.document_pairing import import_and_save_document_pair
from translation_service.models import TranslationUnit
from tempfile import NamedTemporaryFile
from translation_service.docx_parser import extract_paragraphs

from docx.opc.exceptions import PackageNotFoundError

from translation_service.translation_memory import find_exact_match

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
    return {
        "service": PROJECT_NAME,
        "version": VERSION,
        "status": "running",
        "docker": "running",
    }


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "running",
        "database": "connected",
        "docker": "running",
    }


@app.get("/translation-units")
def get_translation_units(
    db: Session = Depends(get_db),
):
    units = db.query(TranslationUnit).order_by(TranslationUnit.id.desc()).all()

    if units is None:
        raise RuntimeError("No TranslationUnit found")

    return [
        {
            "id": unit.id,
            "source_text": unit.source_text,
            "target_text": unit.target_text,
        }
        for unit in units
    ]


@app.post("/docx/parse")
async def parse_docx(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing",
        )

    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Only DOCX files are supported",
        )

    with NamedTemporaryFile(
        delete=False,
        suffix=".docx",
    ) as temp_file:
        temp_file.write(await file.read())
        temp_path = Path(temp_file.name)

    try:
        paragraphs = extract_paragraphs(temp_path)

        return {
            "paragraph_count": len(paragraphs),
            "paragraphs": paragraphs,
        }

    except PackageNotFoundError:
        raise HTTPException(
            status_code=422,
            detail="Invalid DOCX file",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to parse document",
        )

    finally:
        Path(temp_path).unlink(missing_ok=True)


@app.post("/document-pairs/import")
async def import_document_pair_endpoint(
    source_file: UploadFile = File(...),
    target_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not source_file.filename or not target_file.filename:
        raise HTTPException(
            status_code=400,
            detail="Both files must have filenames",
        )

    if not source_file.filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Source file must be a DOCX document",
        )

    if not target_file.filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Target file must be a DOCX document",
        )

    with NamedTemporaryFile(delete=False, suffix=".docx") as source_temp:
        source_temp.write(await source_file.read())
        source_path = Path(source_temp.name)

    with NamedTemporaryFile(delete=False, suffix=".docx") as target_temp:
        target_temp.write(await target_file.read())
        target_path = Path(target_temp.name)

    try:
        imported_count = import_and_save_document_pair(
            source_path,
            target_path,
            source_file.filename,
            target_file.filename,
            db,
        )

        return {
            "source_document": source_file.filename,
            "target_document": target_file.filename,
            "imported_segments": imported_count,
        }

    except PackageNotFoundError as exc:
        raise HTTPException(
            status_code=422,
            detail="Invalid DOCX file",
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    finally:
        Path(source_path).unlink(missing_ok=True)
        Path(target_path).unlink(missing_ok=True)


@app.get("/translations/exact")
def get_exact_match(
    source_text: str,
    db: Session = Depends(get_db),
):
    translation = find_exact_match(
        source_text,
        db,
    )

    return {
        "source_text": source_text,
        "target_text": translation,
    }
