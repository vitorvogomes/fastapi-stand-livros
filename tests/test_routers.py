import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from db.book_models import Book_Model
from main import app


# Mock do serviço BookService
mock_book_service = MagicMock()

# Mock do get_db
@pytest.fixture
def mock_get_db():
    mock_session = MagicMock(spec=Session)
    yield mock_session

# Configurando o TestClient
client = TestClient(app)

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
    assert books[0]["titulo"] == "Book1"  # Verifica o título do primeiro livro

# Função de teste para criar livros
def test_create_books_success(mock_get_db):
    # Criando uma instância mock do Book_Model
    mock_book = Book_Model(
        book_id="1",
        book_title="Book1",
        book_author="Author 1",
        book_category="Ficção",
        book_price=99.99
    )

    # Configurando o mock para retornar o mock_book ao chamar o método create_book
    mock_book_service.create_book.return_value = mock_book

    # Payload para criar um livro
    payload = [{
        "book_id": "1",  # Adicione um ID único para o livro
        "book_title": "Book1",
        "book_author": "Author 1",
        "book_category": "Ficção",
        "book_price": 99.99
    }]
    
    # Chama o endpoint POST para criar o livro
    response = client.post("/books", json=payload)
    
    # Verificando se o status da resposta é 201 (Created)
    assert response.status_code == 201  # Esperando o status 201 de criação
    
    # Verificando se a resposta JSON contém o sucesso esperado
    assert response.json()["success"] == "Novos livros criados com sucesso"
    
    # Verificando se os dados retornados estão corretos
    assert response.json()["data"][0]["id"] == "1"
    assert response.json()["data"][0]["titulo"] == "Book1"
    assert response.json()["data"][0]["autor"] == "Author 1"
    assert response.json()["data"][0]["categoria"] == "Ficção"
    assert response.json()["data"][0]["valor"] == 99.99

def test_put_or_create_book_success(mock_get_db):
    # Criando uma instância mock do Book_Model
    mock_book = Book_Model(
        book_id="1",
        book_title="Book1",
        book_author="Author 1",
        book_category="Aventura",  # Atualizando a categoria
        book_price=99.99
    )

    # Configurando o mock para retornar o mock_book ao chamar o método update_book
    mock_book_service.update_book.return_value = mock_book

    # Payload para atualizar o livro
    payload = {
        "book_id": "1",  # ID único do livro
        "book_title": "Book1",
        "book_author": "Author 1",
        "book_category": "Ficção",  # Categoria enviada no payload
        "book_price": 99.99
    }
    
    # Chama o endpoint PUT para criar ou atualizar o livro
    response = client.put("/books", json=payload)
    
    # Verificando se o status da resposta é 200 (OK)
    assert response.status_code == 200  # Esperando o status 200 de sucesso
    
    # Verificando se a mensagem de sucesso está correta
    assert "Livro criado ou atualizado com sucesso" in response.json()["success"]
    
    # Verificando se os dados retornados estão corretos
    assert response.json()["data"]["id"] == "1"
    assert response.json()["data"]["titulo"] == "Book1"
    assert response.json()["data"]["autor"] == "Author 1"
    assert response.json()["data"]["categoria"] == "Aventura"  # A categoria foi atualizada
    assert response.json()["data"]["valor"] == 99.99

def test_get_book_by_id_success(mock_get_db):
    # Criando uma instância mock do Book_Model
    mock_book = Book_Model(
        book_id="1",
        book_title="Book1",
        book_author="Author 1",
        book_category="Ficção",
        book_price=99.99
    )

    # Configurando o mock para retornar o mock_book ao chamar o método get_book
    mock_book_service.get_book.return_value = mock_book

    # Chama o endpoint GET para buscar o livro pelo ID
    response = client.get("/books/1")

    # Verificando se o status da resposta é 200 (OK)
    assert response.status_code == 200  # Esperando o status 200 de sucesso
    
    # Verificando se a mensagem de sucesso está correta
    assert response.json()["success"] == "Livro encontrado"
    
    # Verificando se os dados retornados estão corretos
    assert response.json()["data"]["id"] == "1"
    assert response.json()["data"]["titulo"] == "Book1"
    assert response.json()["data"]["autor"] == "Author 1"
    assert response.json()["data"]["categoria"] == "Ficção"
    assert response.json()["data"]["valor"] == 99.99

def test_delete_book_by_id_success(mock_get_db):
    # Criando uma instância mock do Book_Model
    mock_book = Book_Model(
        book_id="1",
        book_title="Book1",
        book_author="Author 1",
        book_category="Ficção",
        book_price=99.99
    )

    # Configurando o mock para retornar o mock_book ao chamar o método get_book
    mock_book_service.get_book.return_value = mock_book

    # Configurando o mock para simular a deleção do livro
    mock_book_service.delete_book.return_value = {"id": "1", "titulo": "Book1", "autor": "Author 1", "categoria": "Ficção", "valor": 99.99}

    # Chama o endpoint DELETE para deletar o livro pelo ID
    response = client.delete("/books/1")

    # Verificando se o status da resposta é 200 (OK)
    assert response.status_code == 200  # Esperando o status 200 de sucesso
    
    # Verificando se a mensagem de sucesso está correta
    assert "Livro deletado" in response.json()["success"]
    
    # Verificando se os dados retornados estão corretos
    assert response.json()["data"]["id"] == "1"
    assert response.json()["data"]["titulo"] == "Book1"
    assert response.json()["data"]["autor"] == "Author 1"
    assert response.json()["data"]["categoria"] == "Ficção"
    assert response.json()["data"]["valor"] == 99.99

