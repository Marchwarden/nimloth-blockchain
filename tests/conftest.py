import pytest
from flask import Flask 
from flask.testing import FlaskClient
from core import create_app  # pylint: disable=import-error

@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
