import pytest
from core import create_app
from core.blockchain import Blockchain


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def blockchain():
    return Blockchain()
