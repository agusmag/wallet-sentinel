import pytest

from app import create_app
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app


def test_example(client):
    response = client.get("/")
    print(response.status)
    assert response.status == "200 OK"