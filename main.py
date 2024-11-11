from fastapi import FastAPI
from routers.book_routers import book_router
from db.config import Base, engine

# Criação da aplicação FastAPI com parâmetros de documentação da API Swagger
app = FastAPI (
    title="Documentação StandLivros",
    version="1.0",
    description="""
        API para gerenciamento de um stand de livros, onde é possível realizar operações básicas de CRUD (Create, Read, Update, Delete).
        
        A entidade principal gerenciada pela API é o livro, com os seguintes atributos:
        
        - Título: O título do livro.
        - Autor: O autor do livro.
        - Categoria: A categoria do livro.
        - Preço: O preço de venda do livro.
        
        Funcionalidades
        - Listar livros: Retorna todos os livros ou filtra por título, autor ou categoria.
        - Criar livros: Permite criar um ou mais livros no sistema.
        - Atualizar ou Criar livros: Atualiza as informações de um livro existente ou cria um novo livro se não houver correspondente.
        - Deletar livros: Permite a exclusão de um livro existente baseado no ID.
        
        Para mais informações, consulte a documentação completa abaixo.
    """,
    contact={
        "name": "Vitor Gomes",
        "url": "https://github.com/vitorvogomes",
        "email": "vitorcggomes777@gmail.com"
    }
)

# Roteadores definidos no módulo `book_routers`
app.include_router(book_router)

# Criar as tabelas no banco de dados se ainda não existirem
Base.metadata.create_all(bind=engine)

# Iniciar servidor FastAPI usando Uvicorn
if __name__ == '__main__':
    import uvicorn

    # Configuração do servidor para rodar localmente
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)