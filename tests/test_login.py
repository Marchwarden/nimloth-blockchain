from flask.testing import FlaskClient


def test_login(client: FlaskClient):
    assert client.get("/login").status_code == 200

    response = client.post(
        "/login",
        data={
            "username": "username",
        },
    )

    assert response.status_code == 200
