from flask.testing import FlaskClient


def test_home(client: FlaskClient):
    assert client.get("/home").status_code == 200
