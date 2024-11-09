from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from services.book_service import Book_List, Book_By_Id, Book_Delete, Book_Create
from db.book_schemas import BookModel
from typing import List
from db.config import get_db

# Instância dos serviços responsáveis por gerenciar os livros
book_list_service = Book_List()
book_by_id_service = Book_By_Id()
book_delete_service = Book_Delete()
book_create_service = Book_Create()

# Roteador principal para gerenciar endpoints relacionados aos livros
book_router = APIRouter()

# Rota raiz da aplicação que retorna uma mensagem de boas-vindas
@book_router.get("/")
async def root():
    return {"message": "Welcome to Rack for Books"}

# Endpoint para obter a lista de livros disponíveis
@book_router.get("/books",  
            status_code=status.HTTP_200_OK,
            description="Retorna os livros disponíveis no banco de dados",
            summary="Retorna os livros",
            response_description="Livros encontrados com sucesso")

async def get_books(db: Session = Depends(get_db)):
    try:
        book_list = book_list_service.get(db)
        if not book_list:
            return {"warning": "Nenhum livro cadastrado no banco de dados"}
        return book_list
    except Exception as error:
        # Captura erros gerais e retorna uma resposta 500 (erro interno)
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        )
    
# Endpoint para adicionar um ou mais novos livros
@book_router.post("/books", 
                  status_code=status.HTTP_201_CREATED,
                  description="Cria um ou mais novos livros no banco de dados",
                  summary="Cria novos livros",
                  response_description="Novos livros criados com sucesso")
async def create_book(books: List[BookModel], db: Session = Depends(get_db)):
    try:
        payload = [data.model_dump() for data in books]
        new_books = book_create_service.post(db, payload)
        return new_books
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{error}"
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        )

# Endpoint para buscar detalhes de um livro específico pelo seu ID
@book_router.get("/books/{book_id}",
            status_code=status.HTTP_200_OK,
            description="Obtem informações de um livro que foi adicionado no banco de dados através do seu ID",
            summary="Busca um livro pelo ID",
            response_description="O livro foi encontrado")

async def get_book_by_id(book_id: str, db: Session = Depends(get_db)):
    try:
        book = book_by_id_service.get(db, book_id)
        if not book:
            return {"warning": f"O livro com o id: {book_id} não foi localizado."}
        return book
    except Exception as error:
        # Captura erros gerais e retorna uma resposta 500 (erro interno)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        )

# Endpoint para deletar um livro específico pelo seu ID
@book_router.delete("/books/{book_id}",
                    status_code=status.HTTP_200_OK,
                    description="Deleta um livro que foi adicionado no banco de dados através do seu ID",
                    summary="Deleta um livro pelo ID",
                    response_description="Livro deletado com sucesso.")
async def delete_book_by_id(book_id: str, db: Session = Depends(get_db)):
    try:
        book = book_by_id_service.get(db, book_id)
        if not book:
            return {"warning": f"O livro com o id: {book_id} não foi localizado."}
        book_delete_service.delete(db, book_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        )