from flask.testing import FlaskClient


def test_redirect(client: FlaskClient):
    assert client.get("/").status_code == 302
    assert client.get("/").headers["Location"] == "/home"


data = {
    "username": "username",
    "sender": "sender",
    "receiver": "receiver",
    "amount": "amount",
    "coin": "coin",
    "submit_button": "",
}


def test_home(client: FlaskClient):
    assert client.get("/home").status_code == 200


def test_invalid_post(client: FlaskClient):
    invalid_post_response = client.post(
        "/home",
        data=data,
    )
    assert invalid_post_response.status_code == 400


def test_add_current_block(client: FlaskClient):
    data["submit_button"] = "add_current_block"
    add_current_block_response = client.post(
        "/home",
        data=data,
    )
    assert add_current_block_response.status_code == 200


def test_add_current_transaction(client: FlaskClient):
    data["submit_button"] = "add_current_transaction"
    add_current_transaction_response = client.post(
        "/home",
        data=data,
    )
    assert add_current_transaction_response.status_code == 200
