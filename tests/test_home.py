from flask.testing import FlaskClient

def test_redirect(client: FlaskClient): 
  assert client.get('/').status_code == 302
  assert client.get('/').headers["Location"] == "/home"

def test_home(client: FlaskClient): 
  assert client.get('/home').status_code == 200 