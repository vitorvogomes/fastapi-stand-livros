from sqlalchemy import Column, String, Float
from db.config import Base

# Modelo SQLAlchemy que representa a tabela `RackData` no banco de dados PostgreSQL
class Book_Model(Base):
    __tablename__ = 'RackData'

    # Definição das colunas da tabela
    book_id = Column(String, primary_key=True, index=True)
    book_title = Column(String, index=True)
    book_author = Column(String, index=True)
    book_category = Column(String, index=True)
    book_price = Column(Float)

    # Construtor da classe `Book_Model` que inicializa um objeto livro.
    def __init__(self, book_id, book_title, book_author, book_category, book_price):
        self.book_id = book_id
        self.book_title = book_title
        self.book_author = book_author
        self.book_category = book_category
        self.book_price = book_price

    # Método que retorna os dados do livro no formato JSON.
    def json(self):
        return {
            "id": self.book_id,
            "titulo": self.book_title,
            "autor": self.book_author,
            "categoria": self.book_category,
            "valor": self.book_price
        }
        
        
