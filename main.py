from fastapi import FastAPI
from book_routers import book_router

# Criação da aplicação FastAPI com parâmetros de documentação da API Swagger
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

# Roteadores definidos no módulo `book_routers`
app.include_router(book_router)

# Iniciar servidor FastAPI usando Uvicorn
if __name__ == '__main__':
    import uvicorn

    # Configuração do servidor para rodar localmente
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)