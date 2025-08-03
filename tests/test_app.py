import pytest
import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # ou from main import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'In\xc3\xadcio' in response.data  # ajuste conforme o retorno real

def test_404_route(client):
    response = client.get('/rota-inexistente')
    assert response.status_code == 404
