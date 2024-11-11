from sqlalchemy.orm import Session
from db.book_models import Book_Model
from typing import List, Dict, Optional
import uuid
from functools import wraps
from fastapi import HTTPException

# Classe base genérica para operações CRUD
class CrudService:
    def __init__(self, model):
        self.model = model

    # Busca um livro específico no banco de dados pelo seu ID
    def _get_by_id(self, db: Session, entity_id: str):
        return db.query(self.model).filter(self.model.book_id == entity_id).first()

    # Consulta todos os livros no banco de dados
    def _get_list(self, db: Session, filters: Dict[str, Optional[str]]):
        query = db.query(self.model)
        for field, value in filters.items():
            if value:
                query = query.filter(getattr(self.model, field).ilike(f"%{value}%"))
        return query.all()   
    
    # Cria um ou mais livros no banco de dados
    def _create(self, db: Session, data: Dict):
        try:
            entity = self.model(**data)
            db.add(entity)
            db.commit()
            db.refresh(entity) 
            return entity
        except Exception as error:
            raise error

    def _update(self, db: Session, entity_id: str, data: Dict):
        entity = self._get_by_id(db, entity_id)
        if not entity:
            raise ValueError(f"Entity with ID {entity_id} not found")
        for key, value in data.items():
            setattr(entity, key, value)
        db.commit()
        return entity
    
    # Deleta no banco de dados pelo seu ID
    def _delete(self, db: Session, entity_id: str):
        entity = self._get_by_id(db, entity_id)
        if not entity:
            raise ValueError(f"Entity with ID {entity_id} not found")
        db.delete(entity)
        db.commit()
        return entity

# Função decoradora para tratar erros
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))
    return wrapper

# Serviços específicos para cada operação CRUD
class BookService(CrudService):
    def __init__(self):
        super().__init__(Book_Model)

    @handle_exceptions
    def list_books(self, db: Session, titulo: Optional[str] = None, autor: Optional[str] = None, categoria: Optional[str] = None):
        filters = {"book_title": titulo, "book_author": autor, "book_category": categoria}
        books = self._get_list(db, filters)
        if not books:
            raise ValueError(f"No books found with filters: {', '.join(filter(None, filters.values()))}")
        return [book.json() for book in books]

    @handle_exceptions
    def get_book(self, db: Session, book_id: str):
        book = self._get_by_id(db, book_id)
        if not book:
            raise ValueError(f"Book with ID {book_id} not found")
        return book.json()

    @handle_exceptions
    def create_book(self, db: Session, book_data: Dict):
        if self._get_by_id(db, book_data["book_id"]):
            raise ValueError(f"Book with ID {book_data['book_id']} already exists")
        return self._create(db, book_data).json()

    @handle_exceptions
    def update_book(self, db: Session, book_id: str, book_data: Dict):
        return self._update(db, book_id, book_data).json()

    @handle_exceptions
    def delete_book(self, db: Session, book_id: str):
        return self._delete(db, book_id).json()
    


