from pydantic import BaseModel
from typing import Optional

class BookModel(BaseModel):
    id: Optional[str] = None #UUID gerado automaticamente
    nome: str
    autor: str
    valor: float
    categoria: str

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Nome do Livro",
                "autor": "Autor do Livro",
                "categoria": "Categoria do Livro",
                "valor": 99.99,
            }
        }