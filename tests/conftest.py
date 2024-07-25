import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = response.json['token']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return headers
