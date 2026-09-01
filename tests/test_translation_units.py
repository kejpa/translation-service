from fastapi.testclient import TestClient

from translation_service.main import app

client = TestClient(app)


def test_translation_units_endpoint():
    response = client.get("/translation-units")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
