import pytest
from db.config import SessionLocal, engine, Base
from db.book_models import Book_Model


# Inicialização do banco de dados de teste sem nenhum livro cadastrado
@pytest.fixture(scope="module")
def test_empty_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Limpa os dados anteriores antes de adicionar novos livros
    db.query(Book_Model).delete()
    db.commit()
    
    yield db  # Banco vazio
    
    db.close()

# Inicialização do banco de dados de teste com apenas um livro cadastrado
@pytest.fixture(scope="module")
def test_one_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Limpa os dados anteriores antes de adicionar novos livros
    db.query(Book_Model).delete()
    db.commit()
    
    book = Book_Model(
        book_id="1",
        book_title="Livro Teste",
        book_author="Autor Teste",
        book_category="Categoria Teste",
        book_price=99.99
    )
    db.add(book)
    db.commit()
    
    yield db
    
    db.close()

# Inicialização do banco de dados de teste varios livros cadastrados
@pytest.fixture(scope="module")
def test_many_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Limpa os dados anteriores antes de adicionar novos livros
    db.query(Book_Model).delete()
    db.commit()
    
    books = [
        Book_Model(
            book_id="1",
            book_title="Livro 1",
            book_author="Autor 1",
            book_category="Categoria 1",
            book_price=50.00
        ),
        Book_Model(
            book_id="2",
            book_title="Livro 2",
            book_author="Autor 2",
            book_category="Categoria 2",
            book_price=60.00
        ),
        Book_Model(
            book_id="3",
            book_title="Livro 3",
            book_author="Autor 3",
            book_category="Categoria 3",
            book_price=70.00
        )
    ]
    
    db.add_all(books)
    db.commit()
    
    yield db
    
    db.close()