from fastapi import FastAPI, status, HTTPException
from books import books

# Define parâmetros para documentação Swagger UI
app = FastAPI (
    title="Stand de Livros",
    version="1.0",
    description="API desenvolvida em FastAPI junto com SQLite3 para realizar operações básicas de CRUD (Create, Read, Update, Delete). A entidade que será gerenciada são Livros presentes em um stand de vendas. Esses livros são definidos pelo Título, Autor, Ano, Sinopse, e Preço.",
    contact={
        "name": "Vitor Gomes",
        "url": "https://github.com/vitorvogomes",
        "email": "vitorcggomes777@gmail.com"
    },
)

@app.get("/")
async def root():
    return {"message": "Welcome to my FastApi Project"}

@app.get("/books",  
            status_code=status.HTTP_200_OK,
            description="Retorna os livros disponíveis no Stand.",
            summary="Retorna livros",
            response_description="Livros encontrados com sucesso.")
async def get_books():
    return {"Livros Disponíveis": books}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)