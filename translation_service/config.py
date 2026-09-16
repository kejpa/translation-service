import os

from dotenv import load_dotenv

load_dotenv()


def get_allowed_origins() -> list[str]:
    origins = os.getenv("ALLOWED_ORIGINS")
    if not origins:
        return []

    return [origin.strip() for origin in origins.split(",") if origin.strip()]


def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "sqlite:///translation_memory.db",
    )


def get_port() -> int:
    return int(
        os.getenv(
            "PORT",
            "8000",
        )
    )


def get_ollama_base_url() -> str:
    return os.getenv(
        "OLLAMA_BASE_URL",
        "http://ollama:11434",
    )


def get_ollama_model() -> str:
    return os.getenv(
        "OLLAMA_MODEL",
        "gemma3:4b",
    )


def get_max_chunk_size() -> int:
    return int(
        os.getenv(
            "MAX_CHUNK_SIZE",
            "4000",
        )
    )


def get_temperature() -> float:
    return float(
        os.getenv(
            "TEMPERATURE",
            "0",
        )
    )


def get_log_level() -> str:
    return os.getenv(
        "LOG_LEVEL",
        "INFO",
    )


def get_reuse_threshold() -> int:
    return int(
        os.getenv(
            "REUSE_THRESHOLD",
            "85",
        )
    )


def get_reference_threshold() -> int:
    return int(
        os.getenv(
            "REFERENCE_THRESHOLD",
            "30",
        )
    )
