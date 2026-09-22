from translation_service.normalization import (
    extract_prefix,
    normalize_text,
    rebuild_text,
)


def test_normalize_sw_rule_number():
    text = "SW 14.4 Useamman kuin kahden sormen teippaus"
    assert normalize_text(text) == ("Useamman kuin kahden sormen teippaus")
    text = "SW 10.2.2	Ei pysynyt koko matkaa omalla radallaan"
    assert normalize_text(text) == ("Ei pysynyt koko matkaa omalla radallaan")


def test_normalize_plain_text():
    text = "Tämä koskee kaikkia opiskelijoita."

    assert normalize_text(text) == text


def test_normalize_removes_leading_whitespace():
    text = "SW 14.4    Useamman kuin kahden sormen teippaus"

    assert normalize_text(text) == ("Useamman kuin kahden sormen teippaus")


def test_normalize_empty_string():
    assert normalize_text("") == ""


def test_extract_sw_rule_prefix():
    prefix, text = extract_prefix(
        "SW 27.8\tUseamman kuin kahden sormen teippaus",
    )

    assert prefix == "SW 27.8"
    assert text == ("Useamman kuin kahden sormen teippaus")


def test_rebuild_text():
    assert (
        rebuild_text(
            "SW 27.8",
            "Tejpning av fler än två fingrar eller tår",
        )
        == "SW 27.8\tTejpning av fler än två fingrar eller tår"
    )
