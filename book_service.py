from sqlalchemy.orm import Session
from book_models import Book_Model

# Classe base genérica para operações CRUD
class BookBaseService:
    def __init__(self, model):
        self.model = model

    # Consulta todos os livros no banco de dados.
    def _get_book_list(self, db: Session):
        return db.query(self.model).all()
    
    # Busca um livro específico no banco de dados pelo seu ID.
    def _get_book_by_id(self, db: Session, book_id: int):
        return db.query(self.model).filter(self.model.book_id == book_id).first()
    
    # Erro genérico para falhas de banco de dados.
    def __handle_db_value_error(self, error):
        raise ValueError(f"Erro no banco de dados: {error}")


# Serviço responsável por listar todos os livros disponíveis
class Book_List(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)
    
    # Retorna uma lista de todos os livros ou None se vazio.
    def get(self, db: Session):
        try:
            books = self._get_book_list(db)
            if books:
                return [data.json() for data in books]
            return None
        except Exception as error:
            self.__handle_db_value_error(error)
        

# Serviço responsável por buscar um livro específico pelo ID        
class Book_By_Id(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)
    
    # Retorna um livro específico pelo ID ou None se não encontrado.
    def get(self, db: Session, book_id: int):
        try:
            book = self._get_book_list(db, book_id)
            if book:
                return book.json()
            return None
        except Exception as error:
            self.__handle_db_value_error(error)

    


