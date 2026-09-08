from translation_service import config


def test_default_threshold_values(
    monkeypatch,
):
    monkeypatch.delenv(
        "REUSE_THRESHOLD",
        raising=False,
    )

    monkeypatch.delenv(
        "REFERENCE_THRESHOLD",
        raising=False,
    )

    assert config.get_reuse_threshold() == 85
    assert config.get_reference_threshold() == 30


def test_thresholds_can_be_overridden(
    monkeypatch,
):
    monkeypatch.setenv(
        "REUSE_THRESHOLD",
        "90",
    )

    monkeypatch.setenv(
        "REFERENCE_THRESHOLD",
        "40",
    )

    assert config.get_reuse_threshold() == 90
    assert config.get_reference_threshold() == 40


def test_get_ollama_model_uses_environment_override(
    monkeypatch,
):
    monkeypatch.setenv(
        "OLLAMA_MODEL",
        "llama3.1:8b",
    )

    assert config.get_ollama_model() == "llama3.1:8b"


def test_get_temperature_uses_environment_override(
    monkeypatch,
):
    monkeypatch.setenv(
        "TEMPERATURE",
        "0.3",
    )

    assert config.get_temperature() == 0.3
