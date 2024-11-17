from pydantic import BaseModel
from typing import List, Optional

class BookModel(BaseModel):
    id: Optional[str] = None #UUID gerado automaticamente
    titulo: str
    autor: str
    categoria: str
    valor: float

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "titulo": "O Senhor dos Anéis",
                "autor": "J.R.R. Tolkien",
                "categoria": "Ficção Fantástica",
                "valor": 59.90
            }
        }

class BookListResponse(BaseModel):
    success: str
    data: List[BookModel]

    class Config:
        json_schema_extra = {
            "example": {
                "success": "Livros encontrados",
                "data": [
                    {
                        "id": "1",
                        "titulo": "O Senhor dos Anéis",
                        "autor": "J.R.R. Tolkien",
                        "categoria": "Ficção Fantástica",
                        "valor": 59.90
                    }
                ]
            }
        }

class NoBooksResponse(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Nenhum livro cadastrado na StandLivros."
            }
        }

class NoBooksWithFiltersResponse(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Nenhum livro encontrado para os filtros aplicados: título, autor."
            }
        }

class ErrorResponse(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Erro ao listar livros: erro inesperado"
            }
        }

class NoBooksWithIdResponse(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Nenhum livro encontrado com o id: '1'"
            }
        }

class ExistingBookResponse(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Já existe um livro com o titulo: 'O Senhor dos Anéis', na categoria: 'Ficção Fantástica'"
            }
        }