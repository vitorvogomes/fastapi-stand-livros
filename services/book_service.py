import uuid
from sqlalchemy import tuple_
from sqlalchemy.orm import Session
from db.book_models import Book_Model
from fastapi import HTTPException, status
from typing import Optional

class BookService:
    def list_books(self, db: Session, titulo: str = None, autor: str = None, categoria: str = None):
        # Lista livros com filtros opcionais
        query = db.query(Book_Model)

        query_filters = []
        if titulo:
            query = query.filter(Book_Model.book_title.ilike(f"%{titulo}%"))
            query_filters.append("título")
        if autor:
            query = query.filter(Book_Model.book_author.ilike(f"%{autor}%"))
            query_filters.append("autor")
        if categoria:
            query = query.filter(Book_Model.book_category.ilike(f"%{categoria}%"))
            query_filters.append("categoria")
               
        books = query.all()
        if not books and not query_filters:
            # Levanta HTTPException com status 404 se nenhum livro for encontrado
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum livro cadastrado na StandLivros"
            )
        
        if not books and query_filters:
            # Levanta HTTPException com status 404 se nenhum livro for encontrado utilizando filtros
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum livro encontrado para os filtros aplicados: {', '.join(query_filters)}."
            )
        
        return {"success": "Livros encontrados", "data": [book.json() for book in books]}

    def get_book(self, db: Session, book_id: str):
        book = db.query(Book_Model).filter(Book_Model.book_id == book_id).first()       
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum livro encontrado com o id: {book_id}"
            )
        return {"success": "Livro encontrado", "data": [book.json()]}

    def create_book(self, db: Session, book_list: list):
        new_books = []
        
        for book in book_list:
            if self.check_book_existence(db, book['titulo'], book['categoria']):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Já existe um livro com o título '{book['titulo']}' na categoria '{book['categoria']}'."
                )
            else:
                new_books.append(
                    Book_Model(
                        book_id=str(uuid.uuid4()),
                        book_title=book['titulo'],
                        book_author=book['autor'],
                        book_category=book['categoria'],
                        book_price=book['valor']
                    )
                )
        
        # Adiciona e comita apenas os livros novos
        db.add_all(new_books)
        db.commit()
        return {"success": f"{len(new_books)} livros adicionados com sucesso", "data": [book.json() for book in new_books]}

    def update_book(self, db: Session, book_data: dict):
        book = self.check_book_existence(db, book_data['titulo'], book_data['categoria'])
        if book:
            # Atualiza o livro existente
            book.book_title = book_data.get('titulo')
            book.book_author = book_data.get('autor')
            book.book_category = book_data.get('categoria')
            book.book_price = book_data.get('valor')
            db.commit()
            return {"success": "Livro atualizado com sucesso", "data": [book.json()]}
        else:
            # Caso o livro não exista, adiciona um novo
            book = Book_Model(
                book_id=str(uuid.uuid4()),  # Gera um novo ID UUID para o livro
                book_title=book_data.get('titulo'),
                book_author=book_data.get('autor'),
                book_category=book_data.get('categoria'),
                book_price=book_data.get('valor')
            )
            db.add(book)
            db.commit()
            return {"success": "Novo livro adicionado com sucesso", "data": [book.json()]}

    def delete_book(self, db: Session, book_id: str):
       # Deleta um livro pelo ID
        book = db.query(Book_Model).filter(Book_Model.book_id == book_id).first()
        
        if book:
            db.delete(book)
            db.commit() # Grava as mudanças
            return {"success": f"Livro deletado com o id: {book_id} com sucesso", "data": []}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum livro encontrado com o id: {book_id}"
        )

    def check_book_existence(self, db: Session, titulo: str, categoria: str) -> Optional[Book_Model]:
        return db.query(Book_Model).filter(
            Book_Model.book_title == titulo,
            Book_Model.book_category == categoria
        ).first()