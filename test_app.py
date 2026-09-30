from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'

def test_home_page():
    r = client.get('/')
    assert r.status_code == 200
    assert 'PocketSmart' in r.text

def test_startup():
    r = client.get('/startup')
    assert r.status_code == 200
