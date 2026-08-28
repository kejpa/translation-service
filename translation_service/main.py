from pathlib import Path
import tomllib

from fastapi import FastAPI

VERSION = Path("VERSION").read_text(encoding="utf-8").strip()

with open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

PROJECT_NAME = pyproject["project"]["name"]
PROJECT_DESCRIPTION = pyproject["project"].get("description", "")

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
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "ok"}