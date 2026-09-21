from translation_service.normalization import (
    normalize_text,
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
