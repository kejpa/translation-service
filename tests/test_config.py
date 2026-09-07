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
