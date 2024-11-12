from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from services.book_service import BookService
from db.book_schemas import BookModel, BookListResponse, ErrorResponse
from typing import List, Optional
from db.config import get_db

# Instância dos serviços responsáveis por gerenciar os livros
book_service = BookService()

# Roteador principal para gerenciar endpoints relacionados aos livros
book_router = APIRouter()

# Rota raiz da aplicação que retorna uma mensagem de boas-vindas
@book_router.get("/",
    description="Retorna uma mensagem de boas vindas",
    summary="Raíz do projeto"
)
async def root():
    return {"message": "Welcome to StandLivros"}

# Endpoint para obter a lista de livros disponíveis
@book_router.get(
    "/books",  
    status_code=status.HTTP_200_OK,
    description="Retorna os livros disponíveis na StandLivros.",
    summary="Retorna os livros.",
    response_description="Livros encontrados",
    response_model= BookListResponse,
    responses={
        404: {
            "description": "Nenhum livro encontrado.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Nenhum livro cadastrado na StandLivros"}
                }
            }
        },
        500: {
            "description": "Erro interno do servidor.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Erro ao listar livros: erro inesperado"}
                }
            }
        },
    }
)
async def get_books(
    db: Session = Depends(get_db),
    titulo: Optional[str] = None,
    autor: Optional[str] = None,
    categoria: Optional[str] = None
):
    try:
        book_list = book_service.list_books(db, titulo=titulo, autor=autor, categoria=categoria)
        return {"success": "Livros disponiveis na StandLivros", "data": book_list}
    except Exception as error:
        # Captura erros gerais e retorna uma resposta 500 (erro interno)
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar livros: {error}"
        )
    
# Endpoint para adicionar um ou mais novos livros
@book_router.post(
    "/books", 
    status_code=status.HTTP_201_CREATED,
    description="Cria um ou mais novos livros na StandLivros",
    summary="Cria novos livros",
    response_description="Novos livros criados",
    response_model= BookListResponse,
    responses={
        409: {
            "description": "Já existe o livro na StandLivros",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Conflito: o livro já existe na StandLivros"}
                }
            }
        },
        500: {
            "description": "Erro interno do servidor.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Erro ao listar livros: erro inesperado"}
                }
            }
        },
    }
)
async def create_book(books: List[BookModel], db: Session = Depends(get_db)):
    try:
        created_books = book_service.create_book(db, [book.model_dump() for book in books])
        return {"success": "Livros criados com sucesso", "data": created_books}
    except HTTPException as error:
        raise error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar livros: {error}"
        )

# Endpoint para atualizar ou criar um livro
@book_router.put("/books",
    status_code=status.HTTP_200_OK,
    description="Atualiza as informações do livro ou caso ele não existir, cria um novo com as informações",
    summary="Atualiza ou Cria um livro",
    response_description="O livro foi atualizado",
    response_model= BookListResponse,
    responses={
        500: {
            "description": "Erro interno do servidor.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Erro ao listar livros: erro inesperado"}
                }
            }
        }
    }
)
async def put_or_create_book(book: BookModel, db: Session = Depends(get_db)):
    try:
        updated_book = book_service.update_book(db, book.model_dump())
        return {"success": "Livro criado ou atualizado com sucesso", "data": [updated_book]}
    except HTTPException as error:
        raise error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar ou criar livros: {error}"
        )

# Endpoint para buscar detalhes de um livro específico pelo seu ID
@book_router.get("/books/{book_id}",
    status_code=status.HTTP_200_OK,
    description="Obtem informações de um livro que foi adicionado na StandLivros através do seu ID",
    summary="Busca um livro pelo ID",
    response_description="O livro foi encontrado",
    response_model= BookListResponse,
    responses={
        404: {
            "description": "Nenhum livro encontrado com id.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Não localizado: Nenhum livro cadastrado com o id na StandLivros"}
                }
            }
        },
        500: {
            "description": "Erro interno do servidor.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Erro ao listar livros: erro inesperado"}
                }
            }
        },
    }
)
async def get_book_by_id(book_id: str, db: Session = Depends(get_db)):
    try:
        book = book_service.get_book(db, book_id)
        return {"success": "Livro encontrado", "data": [book]}
    except HTTPException as error:
        raise error
    except Exception as error:
        # Captura erros gerais e retorna uma resposta 500 (erro interno)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar livro: {error}"
        )

# Endpoint para deletar um livro específico pelo seu ID
@book_router.delete("/books/{book_id}",
    status_code=status.HTTP_200_OK,
    description="Deleta um livro que foi adicionado na StandLivros através do seu ID",
    summary="Deleta um livro pelo ID",
    response_description="Livro deletado",
    response_model= BookListResponse,
    responses={
        404: {
            "description": "Nenhum livro encontrado com id.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Não localizado: Nenhum livro cadastrado com o id na StandLivros"}
                }
            }
        },
        500: {
            "description": "Erro interno do servidor.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Erro ao listar livros: erro inesperado"}
                }
            }
        },
    }
)
async def delete_book_by_id(book_id: str, db: Session = Depends(get_db)):
    try:
        book_service.delete_book(db, book_id)
        return {"success": "Livro deletado", "data": []}
    except HTTPException as error:
        raise error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar livro: {error}"
        )