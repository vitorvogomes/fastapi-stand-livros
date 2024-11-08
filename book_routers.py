from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from book_service import Book_List, Book_By_Id
from config import get_db

# Instância dos serviços responsáveis por gerenciar os livros
book_list_service = Book_List()
book_by_id_service = Book_By_Id()

# Roteador principal para gerenciar endpoints relacionados aos livros
book_router = APIRouter()

# Rota raiz da aplicação que retorna uma mensagem de boas-vindas.
@book_router.get("/")
async def root():
    return {"message": "Welcome to Rack for Books"}

# Endpoint para obter a lista de livros disponíveis.
@book_router.get("/books",  
            status_code=status.HTTP_200_OK,
            description="Retorna os livros disponíveis no Stand.",
            summary="Retorna livros",
            response_description="Livros encontrados com sucesso.")

async def get_books(db: Session = Depends(get_db)):
    try:
        book_list = book_list_service.get(db)
        if not book_list:
            # Retorna um erro 404 caso não haja livros na base de dados
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum livro foi localizado no Rack"
            )
        else:
            return book_list
    except Exception as error:
        # Captura erros gerais e retorna uma resposta 500 (erro interno)
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        )

# Endpoint para buscar detalhes de um livro específico pelo seu ID.
@book_router.get("/books/{book_id}",
            status_code=status.HTTP_200_OK,
            description="Obtem informações de um livro através do seu id",
            summary="Busca um livro pelo id",
            response_description="O livro foi encontrado.")

async def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    try:
        book = book_by_id_service.get(db, book_id)
        if not book:
            # Retorna um erro 404 caso o livro não seja encontrado
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum livro foi localizado no Rack"
            )
        return book
    except Exception as error:
        # Captura erros gerais e retorna uma resposta 500 (erro interno)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        )
