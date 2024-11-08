from sqlalchemy.orm import Session
from book_models import Book_Model

import uuid

# Classe base genérica para operações CRUD
class BookBaseService:
    def __init__(self, model):
        self.model = model

    # Consulta todos os livros no banco de dados
    def _get_book_list(self, db: Session):
        return db.query(self.model).all()
    
    # Busca um livro específico no banco de dados pelo seu ID
    def _get_book_by_id(self, db: Session, book_id: str):
        return db.query(self.model).filter(self.model.book_id == book_id).first()
    
    # Deleta um livro no banco de dados pelo seu ID
    def _delete_book_by_id(self, db: Session, book_id: str):
        book = self._get_book_by_id(db, book_id)
        if not book:
            raise ValueError(f"(service) O livro com o ID {book_id} não foi localizado.")
        db.delete(book)
        db.commit()
        return {"success": f"o livro com o ID {book_id} foi deletado."}
    
    # Verifica se um livro através do título e categoria já existe no banco de dados
    def _check_if_book_exists(self, db: Session, book_title: str, book_category: str):
        return db.query(self.model).filter(
            self.model.book_title == book_title,
            self.model.book_category == book_category
            ).first()
    
    # Cria um ou mais livros no banco de dados
    def _create_books(self, db: Session, books: list[dict]):
        new_books = []
        for data in books:
            # Verifica se o livro já existe no banco de dados
            check = self._check_if_book_exists(db, data["titulo"], data["categoria"])
            if check:
                raise ValueError(f"(service) O livro {data["titulo"]} já existe no banco de dados.")
            
            # Se o livro não existir, adiciona no banco de dados
            book = self.model(
                book_id = str(uuid.uuid4()),
                book_title = data["titulo"],
                book_author = data["autor"],
                book_category = data["categoria"],
                book_price = data["valor"]
            )
            db.add(book)
            new_books.append(book)
        db.commit()
        return [data.json() for data in new_books]
    
    # Erro genérico para falhas de banco de dados
    def __handle_db_value_error(self, error):
        raise ValueError(f"(service) Erro no banco de dados: {error}")


# Serviço responsável por listar todos os livros
class Book_List(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)

    def get(self, db: Session):
        try:
            books = self._get_book_list(db)
            if books:
                return [data.json() for data in books]
            return None
        except Exception as error:
            self.__handle_db_value_error(error)


# Serviço responsável por criar novos livros
class Book_Create(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)

    def post(self, db: Session, books: list[dict]):
        try:
            return self._create_books(db, books)
        except Exception as error:
            self.__handle_db_value_error(error)


# Serviço responsável por buscar um livro específico pelo ID        
class Book_By_Id(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)

    def get(self, db: Session, book_id: str):
        try:
            book = self._get_book_by_id(db, book_id)
            if book:
                return book.json()
            return None
        except Exception as error:
            self.__handle_db_value_error(error)


# Serviço responsável por deletar um livro específico pelo ID
class Book_Delete(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)

    def delete(self, db: Session, book_id: str):
        try:
            return self._delete_book_by_id(db, book_id)
        except Exception as error:
            self.__handle_db_value_error(error)

    


