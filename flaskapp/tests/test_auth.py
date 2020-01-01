import pytest

from app import create_app

@pytest.fixture
def app():
    app = create_app()
    return app


def test_example(client):
    response = client.get("/")
    print(response.status)
    assert response.status == "200 OK"