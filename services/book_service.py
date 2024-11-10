from sqlalchemy.orm import Session
from db.book_models import Book_Model
from typing import List, Dict, Optional
import uuid

# Classe base genérica para operações CRUD
class BookBaseService:
    def __init__(self, model):
        self.model = model

    # Consulta todos os livros no banco de dados
    def _get_book_list(self, db: Session, titulo: Optional[str] = None, autor: Optional[str] = None, categoria: Optional[str] = None):
        query = db.query(self.model)
        
        if titulo:
            query = query.filter(self.model.book_title.ilike(f"%{titulo}%"))
        if autor:
            query = query.filter(self.model.book_author.ilike(f"%{autor}%"))
        if categoria:
            query = query.filter(self.model.book_category.ilike(f"%{categoria}%"))
        
        return query.all()
    
    # Busca um livro específico no banco de dados pelo seu ID
    def _get_book_by_id(self, db: Session, book_id: str):
        return db.query(self.model).filter(self.model.book_id == book_id).first()
    
    # Deleta um livro no banco de dados pelo seu ID
    def _delete_book_by_id(self, db: Session, book_id: str):
        # Verifica se o livro existe
        book = self._get_book_by_id(db, book_id)
        if not book:
            # Lança uma exceção ValueError com uma mensagem customizada se o livro não for encontrado
            raise ValueError(f"(service) O livro com o ID {book_id} não foi localizado.")
        db.delete(book)
        db.commit()
    
    # Verifica se um livro através do título e categoria já existe no banco de dados
    def _check_if_book_exists(self, db: Session, book_title: str, book_category: str):
        return db.query(self.model).filter(
            self.model.book_title == book_title,
            self.model.book_category == book_category
            ).first()
    
    # Cria um ou mais livros no banco de dados
    def _create_books(self, db: Session, books: List[Dict]):
        new_books = []
        for data in books:
            # Verifica se o livro já existe no banco de dados
            check = self._check_if_book_exists(db, data["titulo"], data["categoria"])
            if check:
                raise ValueError(f"(service) O livro {data['titulo']} já existe.")
            
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

    # Atualiza ou cria um livro do banco de dados
    def _update_or_create_book(self, db: Session, book_data: Dict):
        book = self._check_if_book_exists(db, book_data['titulo'], book_data["categoria"])
        if book:
            # Atualiza informações do livro existente
            book.book_title = book_data.get("titulo", book.book_title)
            book.book_author = book_data.get("autor", book.book_author)
            book.book_category = book_data.get("categoria", book.book_category)
            book.book_price = book_data.get("valor", book.book_price)
            pass
        else:
            # Cria um novo livro caso não exista
            book = self.model(
                book_id = str(uuid.uuid4()),
                book_title = book_data["titulo"],
                book_author = book_data["autor"],
                book_category = book_data["categoria"],
                book_price = book_data["valor"]
            )
            db.add(book)
        db.commit()
        return book.json()


# Serviço responsável por listar todos os livros
class Book_List(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)

    def get(self, db: Session, titulo: Optional[str] = None, autor: Optional[str] = None, categoria: Optional[str] = None):
        try:
            books = self._get_book_list(db, titulo, autor, categoria)
            # Se nenhum livro for encontrado, lançar erro indicando qual filtro falhou
            if not books:
                if any([titulo, autor, categoria]):  # Verifica se há parâmetros fornecidos
                    not_found_params = []
                    if titulo:
                        not_found_params.append("título")
                    if autor:
                        not_found_params.append("autor")
                    if categoria:
                        not_found_params.append("categoria")

                    # Criando uma mensagem personalizada de erro
                    param_message = ", ".join(not_found_params)
                    raise ValueError(f"(service) Nenhum livro encontrado com o(s) parâmetro(s): {param_message}.")
                return []
            return [data.json() for data in books]
        except Exception as error:
            raise ValueError(f"{error}")


# Serviço responsável por criar novos livros
class Book_Create(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)

    def post(self, db: Session, books: List[Dict]):
        try:
            return self._create_books(db, books)
        except Exception as error:
            raise ValueError(f"{error}")


# Serviço responsável por buscar um livro específico pelo ID        
class Book_By_Id(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)

    def get(self, db: Session, book_id: str):
        try:
            book = self._get_book_by_id(db, book_id)
            if not book:
                raise ValueError(f"(service) O livro com o ID {book_id} não foi encontrado.")
            return book.json()
        except Exception as error:
            raise ValueError(f"{error}")


# Serviço responsável por deletar um livro específico pelo ID
class Book_Delete(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)

    def delete(self, db: Session, book_id: str):
        try:
            return self._delete_book_by_id(db, book_id)
        except Exception as error:
            raise ValueError(f"{error}")

# Serviço responsável por atualizar ou criar um novo livro
class Book_Update_or_Create(BookBaseService):
    def __init__(self):
        super().__init__(Book_Model)
    
    def put(self, db: Session, book_data: Dict):
        try:
            return self._update_or_create_book(db, book_data)
        except Exception as error:
            raise ValueError(f"{error}")

    


