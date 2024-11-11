import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.config import Base
from db.book_models import Book_Model
from services.book_service import BookService, handle_exceptions

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


def test_create_book(db: Session, book_service: BookService):
    data = {
        "book_id": "123",
        "book_title": "Test Book",
        "book_author": "Test Author",
        "book_category": "Test Category",
        "book_price": 19.99
    }
    result = book_service.create_book(db, data)
    assert result["titulo"] == "Test Book"
    assert result["valor"] == 19.99


def test_get_book(db: Session, book_service: BookService):
    data = {
        "book_id": "123",
        "book_title": "Test Book",
        "book_author": "Test Author",
        "book_category": "Test Category", 
        "book_price": 19.99
    }
    book_service.create_book(db, data)
    result = book_service.get_book(db, "123")
    assert result["id"] == "123"

def test_list_books(db: Session, book_service: BookService):
    data1 = {"book_id": "1", "book_title": "Book 1", "book_author": "Author A", "book_category": "Fiction", "book_price": 19.99}
    data2 = {"book_id": "2", "book_title": "Book 2", "book_author": "Author B", "book_category": "Non-fiction", "book_price": 19.99}

    book_service.create_book(db, data1)
    book_service.create_book(db, data2)

    result = book_service.list_books(db)
    assert len(result) == 2

def test_update_book(db: Session, book_service: BookService):
    data = {"book_id": "1", "book_title": "Old Title", "book_author": "Author", "book_category": "Fiction", "book_price": 19.99}
    book_service.create_book(db, data)

    updated_data = {"book_title": "New Title"}
    result = book_service.update_book(db, "1", updated_data)
    assert result["titulo"] == "New Title"

def test_delete_book(db: Session, book_service: BookService):
    data = {"book_id": "1", "book_title": "Book to delete", "book_author": "Author", "book_category": "Fiction", "book_price": 19.99}
    book_service.create_book(db, data)

    result = book_service.delete_book(db, "1")
    assert result["id"] == "1"

def test_handle_exceptions():
    @handle_exceptions
    def raise_exception():
        raise ValueError("Test Error")

    with pytest.raises(Exception) as excinfo:
        raise_exception()
    assert "Test Error" in str(excinfo.value)
