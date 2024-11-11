import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.config import Base
from services.book_service import BookService
from fastapi import HTTPException

# Configuração do banco de dados SQLite em memória para os testes
engine = create_engine("sqlite:///:memory:", echo=True)  # Para ver os logs do SQL executado
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para criar o banco de dados e as tabelas antes dos testes
@pytest.fixture(scope="function")
def db():
    # Cria as tabelas no banco de dados antes de rodar os testes
    Base.metadata.create_all(bind=engine)  # Cria as tabelas a partir do Base
    db = TestingSessionLocal()  # Cria a sessão para interagir com o banco
    yield db  # Executa o teste
    db.close()  # Fecha a sessão
    Base.metadata.drop_all(bind=engine)  # Remove as tabelas após os testes

@pytest.fixture
def book_service():
    return BookService()


def test_create_book_success(db: Session, book_service: BookService):
    data = [
        {
            "titulo": "Test Book",
            "autor": "Test Author",
            "categoria": "Test Category",
            "valor": 19.99
        }
    ]
    result = book_service.create_book(db, data)
    assert len(result) == 1
    assert result[0]["titulo"] == "Test Book"
    assert result[0]["valor"] == 19.99


def test_create_book_conflict(db: Session, book_service: BookService):
    data = [
        {
            "titulo": "Test Book",
            "autor": "Test Author",
            "categoria": "Test Category",
            "valor": 19.99
        }
    ]
    book_service.create_book(db, data)
    
    with pytest.raises(HTTPException) as excinfo:
        book_service.create_book(db, data)
    
    assert excinfo.value.status_code == 409
    assert "Conflito" in excinfo.value.detail



def test_list_books_with_filters(db: Session, book_service: BookService):
    data1 = {"titulo": "Book A", "autor": "Author A", "categoria": "Fiction", "valor": 19.99}
    data2 = {"titulo": "Book B", "autor": "Author B", "categoria": "Non-fiction", "valor": 29.99}

    book_service.create_book(db, [data1, data2])
    
    result = book_service.list_books(db, titulo="Book A")
    assert len(result) == 1
    assert result[0]["titulo"] == "Book A"


def test_list_books_empty(db: Session, book_service: BookService):
    result = book_service.list_books(db)
    assert result == []


def test_update_existing_book(db: Session, book_service: BookService):
    data = {"titulo": "Book Title", "autor": "Author", "categoria": "Category", "valor": 19.99}
    book = book_service.create_book(db, [data])[0]

    update_data = {"id": book["id"], "titulo": "Updated Title"}
    result = book_service.update_book(db, update_data)

    assert result["titulo"] == "Updated Title"


def test_update_create_new_book(db: Session, book_service: BookService):
    update_data = {"id": "non-existent-id", "titulo": "New Book", "autor": "Author", "categoria": "Category", "valor": 15.99}
    result = book_service.update_book(db, update_data)

    assert result["titulo"] == "New Book"
    assert result["valor"] == 15.99


def test_delete_existing_book(db: Session, book_service: BookService):
    data = {"titulo": "Book Title", "autor": "Author", "categoria": "Category", "valor": 19.99}
    book = book_service.create_book(db, [data])[0]

    result = book_service.delete_book(db, book["id"])
    assert result["success"] == "Livro deletado com sucesso"


def test_delete_non_existent_book(db: Session, book_service: BookService):
    with pytest.raises(HTTPException) as excinfo:
        book_service.delete_book(db, "non-existent-id")
    
    assert excinfo.value.status_code == 404
    assert "Nenhum livro encontrado" in excinfo.value.detail
