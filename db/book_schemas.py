from pydantic import BaseModel
from typing import Optional, List

class BookModel(BaseModel):
    id: Optional[str] = None #UUID gerado automaticamente
    titulo: str
    autor: str
    categoria: str
    valor: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "titulo": "O Senhor dos Anéis",
                "autor": "J.R.R. Tolkien",
                "categoria": "Ficção Fantástica",
                "valor": 59.90
            }
        }

class BookResponse(BaseModel):
    id: str
    titulo: str
    autor: str
    categoria: str
    valor: float

class BookListResponse(BaseModel):
    success: str
    data: List[BookResponse]

class ErrorResponse(BaseModel):
    detail: str