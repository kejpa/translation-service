from starlette.testclient import TestClient

from tests.helpers import add_translation
from translation_service.main import app
from translation_service.models import TranslationUnit

client = TestClient(app)


def test_search_translation_units(
    db,
):
    add_translation(
        db,
        "Hei maailma",
        "Hei maailma",
        "Hej världen",
        "Hej världen",
    )

    add_translation(
        db,
        "Miten voit?",
        "Miten voit?",
        "Hur mår du?",
        "Hur mår du?",
    )

    response = client.get(
        "/translation-units?query=maailma",
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": 1,
            "source_text": "Hei maailma",
            "target_text": "Hej världen",
        },
    ]


def test_search_translation_units_returns_empty_result():
    response = client.get(
        "/translation-units?query=foo",
    )

    assert response.status_code == 200
    assert response.json() == []


def test_update_translation_unit(
    db,
):
    add_translation(
        db,
        "Hei maailma",
        "Hei maailma",
        "Hej världen",
        "Hej världen",
    )

    response = client.put(
        "/translation-units/1",
        json={
            "source_text": "Hei maailma",
            "target_text": "Hej världen!!!",
        },
    )

    assert response.status_code == 200

    units = db.query(TranslationUnit).all()

    assert units[0].target_text == ("Hej världen!!!")


def test_delete_translation_unit(
    db,
):
    add_translation(
        db,
        "Hei maailma",
        "Hei maailma",
        "Hej världen",
        "Hej världen",
    )

    response = client.delete(
        "/translation-units/1",
    )

    assert response.status_code == 204

    units = db.query(
        TranslationUnit,
    ).all()

    assert units == []
