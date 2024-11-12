import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from db.book_models import Book_Model
from main import app

# Mock do serviço BookService
mock_book_service = MagicMock()

# Mock da sessão do banco de dados
@pytest.fixture
def mock_get_db():
    mock_session = MagicMock(spec=Session)
    yield mock_session

# Configurando o TestClient
client = TestClient(app)

# Substitui dependências reais por mocks durante os testes
@pytest.fixture(autouse=True)
def setup_dependencies():
    with patch("services.book_service.BookService", return_value=mock_book_service):
        with patch("db.config.get_db", mock_get_db):
            yield

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to StandLivros"}

def test_get_books_success(mock_get_db):
    mock_book_service.list_books.return_value = [
        {"id": "1", "titulo": "Book1", "autor": "Author 1", "categoria": "Ficção", "valor": 99.99},
        {"id": "2", "titulo": "Book2", "autor": "Author 2", "categoria": "Aventura", "valor": 99.99},
        {"id": "3", "titulo": "Book3", "autor": "Author 3", "categoria": "Romance", "valor": 99.99}
    ]
    db = mock_get_db  # Use o mock de db
    books = mock_book_service.list_books(db)
    assert len(books) == 3  # Verifica se os livros foram retornados corretamente
    assert books[0]["titulo"] == "Book1"  # Verifica o título do primeiro livr

def test_create_books_success():
    payload = [
        {"titulo": "Book1", "autor": "Author 1", "categoria": "Ficção", "valor": 99.99}
    ]

    mock_book_service.create_book.return_value = [
        {"id": "1", "titulo": "Book1", "autor": "Author 1", "categoria": "Ficção", "valor": 99.99}
    ]

    response = client.post("/books", json=payload)
    assert response.status_code == 409

def test_put_or_create_book_success():
    payload = {
        "id": "1",
        "titulo": "Book1",
        "autor": "Author 1",
        "categoria": "Aventura",
        "valor": 99.99
    }

    mock_book_service.update_book.return_value = {
        "id": "1",
        "titulo": "Book1",
        "autor": "Author 1",
        "categoria": "Aventura",
        "valor": 99.99
    }

    response = client.put("/books", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] == "Livro criado ou atualizado com sucesso"
    assert response.json()["data"][0]["categoria"] == "Aventura"

def test_get_book_by_id_success():
    mock_book_service.get_book.return_value = {
        "id": "1",
        "titulo": "Book1",
        "autor": "Author 1",
        "categoria": "Ficção",
        "valor": 99.99
    }

    response = client.get("/books/1")
    assert response.status_code == 404

def test_delete_book_by_id_success():
    mock_book_service.delete_book.return_value = {
        "success": "Livro deletado com sucesso",
        "data": []
    }

    response = client.delete("/books/1")
    assert response.status_code == 404
