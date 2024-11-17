import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.config import Base
from services.book_service import BookService
from db.book_models import Book_Model

# Configuração do banco de dados SQLite em memória para os testes
engine = create_engine("sqlite:///:memory:", echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para criar o banco de dados e as tabelas antes dos testes
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)  # Cria as tabelas a partir do Base
    db = TestingSessionLocal()  # Cria a sessão para interagir com o banco
    yield db  # Executa o teste
    db.close()  # Fecha a sessão
    Base.metadata.drop_all(bind=engine)  # Remove as tabelas após os testes

# Instancia o serviço 'BookService' que será testado
@pytest.fixture
def book_service():
    return BookService()

# Dados simulados
data = [
    {
        "titulo": "Test Book 1",
        "autor": "Author 1",
        "categoria": "Category 1",
        "valor": 10.99
    },
    {
        "titulo": "Test Book 2",
        "autor": "Author 2",
        "categoria": "Category 2",
        "valor": 15.99
    }
]

@pytest.fixture
def setup_data(db):
    """Popula o banco de dados com livros simulados."""
    books = [
        Book_Model(
            book_id=str(index + 1),  # Garante IDs únicos para cada livro,
            book_title=book["titulo"],
            book_author=book["autor"],
            book_category=book["categoria"],
            book_price=book["valor"]
        ) for index, book in enumerate(data)
    ]
    db.add_all(books)
    db.commit()

@pytest.mark.parametrize("titulo,expected_count", [("Test Book 1", 1), ("Nonexistent", 0)])
def test_list_books(db, book_service: BookService, setup_data, titulo, expected_count):
    response = book_service.list_books(db, titulo=titulo)
    if expected_count > 0:
        assert response["success"] == "Livros encontrados"
    else:
        assert response["warning"] == "Nenhum livro encontrado."
    assert len(response["data"]) == expected_count

def test_get_book(db, book_service: BookService, setup_data):
    response = book_service.get_book(db, "1")
    assert response["success"] == "Livro encontrado"
    assert response["data"][0]["titulo"] == "Test Book 1"

    response = book_service.get_book(db, "nonexistent")
    assert response["warning"] == "Nenhum livro encontrado com o id: nonexistent"

def test_create_book(db, book_service: BookService):
    new_books = [{"titulo": "New Book", "autor": "New Author", "categoria": "New Category", "valor": 20.00}]
    response = book_service.create_book(db, new_books)
    assert response["success"].startswith("1 livros adicionados")
    
    response = book_service.create_book(db, new_books)
    assert response["warning"] == "Nenhum novo livro adicionado."

def test_update_book(db, book_service: BookService, setup_data):
    updated_data = {"id": "1", "titulo": "Updated Title", "autor": "Author 1", "categoria": "Category 1", "valor": 12.00}
    response = book_service.update_book(db, updated_data)
    assert response["success"] == "Livro atualizado com sucesso"
    assert response["data"]["titulo"] == "Updated Title"

    new_data = {"id": "new_id", "titulo": "New Book", "autor": "New Author", "categoria": "New Category", "valor": 22.00}
    response = book_service.update_book(db, new_data)
    assert response["success"] == "Novo livro adicionado com sucesso"

def test_delete_book(db, book_service: BookService, setup_data):
    response = book_service.delete_book(db, "1")
    assert response["success"] == "Livro deletado com o id: 1 com sucesso"

    response = book_service.delete_book(db, "nonexistent")
    assert response["warning"] == "Livro com o id: nonexistent não encontrado"