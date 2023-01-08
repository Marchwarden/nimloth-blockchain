from flask.testing import FlaskClient


def test_save(client: FlaskClient):
    response = client.get("/save")
    assert response.status_code == 200
    assert response.data == b"blockchain saved"
