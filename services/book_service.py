import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.book_models import Book_Model
from fastapi import HTTPException, status

class BookService:
    def list_books(self, db: Session, titulo: str = None, autor: str = None, categoria: str = None):
        query = db.query(Book_Model)
        
        if titulo:
            query = query.filter(Book_Model.book_title.ilike(f"%{titulo}%"))
        if autor:
            query = query.filter(Book_Model.book_author.ilike(f"%{autor}%"))
        if categoria:
            query = query.filter(Book_Model.book_category.ilike(f"%{categoria}%"))
        
        books = query.all()
        
        # Retorna uma lista vazia caso nenhum livro seja encontrado
        return [book.json() for book in books] if books else []

    def get_book(self, db: Session, book_id: str):
        book = db.query(Book_Model).filter(Book_Model.book_id == book_id).first()
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum livro encontrado com o id fornecido"
            )
        
        return book.json()

    def create_book(self, db: Session, books: list):
        try:
            new_books = []
            for book_data in books:
                # Verifica se já existe um livro com o mesmo título e categoria
                existing_book = db.query(Book_Model).filter(
                    Book_Model.book_title == book_data.get('titulo'),  # Usando .get() para evitar erros
                    Book_Model.book_category == book_data.get('categoria')
                ).first()
                
                if existing_book:
                    raise ValueError(f"Conflito: o livro '{book_data.get('titulo')}' já existe na categoria '{book_data.get('categoria')}'")
                
                # Gera um novo ID UUID para o livro
                new_book_id = str(uuid.uuid4())
                
                new_book = Book_Model(
                    book_id=new_book_id,
                    book_title=book_data.get('titulo'),
                    book_author=book_data.get('autor'),
                    book_category=book_data.get('categoria'),
                    book_price=book_data.get('valor')
                )
                
                db.add(new_book)
                new_books.append(new_book)
            db.commit()
            return [book.json() for book in new_books]
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao tentar adicionar livros ao banco de dados"
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error)
            )
        except Exception as error:
            # Reverte qualquer mudança não confirmada no banco de dados
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar livros: {str(error)}"
            )

    def update_book(self, db: Session, book_data: dict):
        try:
            # Certifique-se de que book_data seja um dicionário
            if not isinstance(book_data, dict):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Os dados do livro devem ser passados como um dicionário"
                )

            book = db.query(Book_Model).filter(Book_Model.book_id == book_data.get('id')).first()

            if book:
                # Atualiza o livro existente
                book.book_title = book_data.get('titulo')
                book.book_author = book_data.get('autor')
                book.book_category = book_data.get('categoria')
                book.book_price = book_data.get('valor')
                db.commit()
                return book.json()
            else:
                # Caso o livro não exista, cria um novo
                new_book_id = str(uuid.uuid4())  # Gera um novo ID UUID para o livro
                new_book = Book_Model(
                    book_id=new_book_id,
                    book_title=book_data.get('titulo'),
                    book_author=book_data.get('autor'),
                    book_category=book_data.get('categoria'),
                    book_price=book_data.get('valor')
                )
                db.add(new_book)
                db.commit()
                return new_book.json()
        except Exception as error:
            # Reverte qualquer mudança não confirmada no banco de dados
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar ou criar livro: {str(error)}"
            )

    def delete_book(self, db: Session, book_id: str):
        try:
            book = db.query(Book_Model).filter(Book_Model.book_id == book_id).first()
            
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nenhum livro encontrado com o id fornecido"
                )
            
            db.delete(book)
            db.commit() # Grava as mudanças, se tudo correr bem
            return {"success": "Livro deletado com sucesso", "data": []}
        except HTTPException:
            # Repassa a exceção para manter o comportamento esperado
            raise
        except Exception as error:
            # Reverte qualquer mudança não confirmada no banco de dados
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao deletar livro: {str(error)}"
            )

