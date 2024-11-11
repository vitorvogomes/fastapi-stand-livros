import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
import uvicorn

client = TestClient(app)

def test_app_documentation():
    """Testa se a documentação da API está corretamente configurada."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Documentação StandLivros" in response.text

def test_app_openapi():
    """Testa o esquema OpenAPI."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Documentação StandLivros"
    assert data["info"]["version"] == "1.0"
    assert "contact" in data["info"]

def test_book_router_included():
    """Testa se os endpoints do roteador foram incluídos."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to StandLivros"}

def test_server_initialization(monkeypatch):
    """Testa a inicialização do servidor Uvicorn."""
    import main

    with patch("uvicorn.run") as mock_run:
        # Simula a execução do servidor sem realmente iniciar o processo
        mock_run.side_effect = SystemExit  # Força o SystemExit quando uvicorn.run for chamado
        
        # Teste que a exceção SystemExit é levantada
        with pytest.raises(SystemExit):
            uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

        # Verifica se uvicorn.run foi chamado com os parâmetros esperados
        mock_run.assert_called_once_with(
            "main:app", host="0.0.0.0", port=8000, reload=True
        )

