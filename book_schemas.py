from pydantic import BaseModel
from typing import Optional

class BookModel(BaseModel):
    id: Optional[int] = None
    nome: str
    autor: str
    valor: float
    categoria: str

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Nome do Livro",
                "autor": "Autor do Livro",
                "valor": 99.99,
                "categoria": "Categoria do Livro"
            }
        }