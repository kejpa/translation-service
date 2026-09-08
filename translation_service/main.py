import tomllib
from dataclasses import asdict
from pathlib import Path
from tempfile import NamedTemporaryFile

from docx.opc.exceptions import PackageNotFoundError
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from translation_service.config import get_ollama_model, get_temperature
from translation_service.database import create_tables, get_db
from translation_service.document_pairing import import_and_save_document_pair
from translation_service.docx_exporter import translate_document, translate_paragraphs
from translation_service.docx_parser import extract_all_paragraphs, extract_paragraphs
from translation_service.fuzzy_search import find_fuzzy_matches
from translation_service.models import TranslationUnit
from translation_service.ollama_service import OllamaError, generate_text
from translation_service.translation_memory import find_exact_matches
from translation_service.translation_statistics import calculate_translation_statistics

VERSION = Path("VERSION").read_text(encoding="utf-8").strip()

with open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

PROJECT_NAME = pyproject["project"]["name"]
PROJECT_DESCRIPTION = pyproject["project"].get("description", "")

create_tables()


class LlmTestRequest(BaseModel):
    prompt: str


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

    finally:
        Path(temp_path).unlink(missing_ok=True)


@app.post("/docx/translate")
async def translate_docx(
    file: UploadFile = File(...),
    output_filename: str = Form("translated.docx"),
    db: Session = Depends(get_db),
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

    with NamedTemporaryFile(
        delete=False,
        suffix=".docx",
    ) as output_file:
        output_path = Path(output_file.name)

    try:
        translate_document(
            temp_path,
            output_path,
            db,
        )

        return FileResponse(
            path=output_path,
            media_type=(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ),
            filename=output_filename,
        )

    except PackageNotFoundError:
        raise HTTPException(
            status_code=422,
            detail="Invalid DOCX file",
        )

    finally:
        temp_path.unlink(missing_ok=True)


# TODO:
# Remove generated output files after response
# has been sent to the client.
##        output_path.unlink(missing_ok=True)


@app.get("/translations/exact")
def get_exact_matches(
    source_text: str,
    db: Session = Depends(get_db),
):
    translations = find_exact_matches(
        source_text,
        db,
    )

    return {
        "source_text": source_text,
        "matches": translations,
    }


@app.post("/docx/statistics")
async def translation_statistics(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
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
        source_paragraphs = extract_all_paragraphs(
            temp_path,
        )

        translations = translate_paragraphs(
            source_paragraphs,
            db,
        )

        statistics = calculate_translation_statistics(
            translations,
        )

        return asdict(statistics)

    except PackageNotFoundError:
        raise HTTPException(
            status_code=422,
            detail="Invalid DOCX file",
        )

    finally:
        temp_path.unlink(missing_ok=True)


@app.get("/translations/fuzzy")
def fuzzy_matches(
    source_text: str,
    db: Session = Depends(get_db),
):
    matches = find_fuzzy_matches(
        source_text,
        db,
    )

    return {
        "source_text": source_text,
        "matches": [
            {
                "id": match.translation_unit.id,
                "document_pair_id": (match.translation_unit.document_pair_id),
                "source_text": (match.translation_unit.source_text),
                "target_text": (match.translation_unit.target_text),
                "score": match.score,
            }
            for match in matches
        ],
    }


@app.post("/llm/test")
def llm_test(
    request: LlmTestRequest,
):
    try:
        return {
            "response": generate_text(
                request.prompt,
            ),
        }

    except OllamaError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error


@app.get("/llm/config")
def llm_config():
    return {
        "model": get_ollama_model(),
        "temperature": get_temperature(),
    }
