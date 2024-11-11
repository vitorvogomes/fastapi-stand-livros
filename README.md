# StandLivros | Python | FastAPI :book:

## Descrição Geral

Neste projeto, será desenvolvido uma **API RESTful** utilizando **FastAPI** em **Python**, realizando operações básicas de CRUD (Create, Read, Update, Delete). 
Implementação de testes unitários, boas práticas de desenvolvimento, recursos de segurança e documentação da API.

### API RESTful FastAPI
- Desenvolver uma API utilizando **FastAPI** para gerenciar uma entidade de "Livros".
- Implementar as operações básicas de **CRUD (Create, Read, Update, Delete)** para essa entidade.
- Utilizar um banco de dados relacional **PostgreSQL**, com uma biblioteca ORM como **SQLAlchemy** para persistência dos dados.

### Cobertura de Testes Unitários
- Implementar **testes unitários** para validar as funcionalidades principais da API.
- Utilizar frameworks de testes como **pytest** para garantir uma cobertura de código de pelo menos 50%, idealmente buscando 100%.

### Autenticação & Autorização
Esses itens não são obrigatórios, mas serão considerados como bônus e podem demonstrar seu nível de experiência e conhecimento avançado:
- Implementar **Autenticação** de usuários utilizando **JWT (JSON Web Tokens)**.
- Implementar a **Autorização** com uso de Dependências (dependencies) ou Middleware para restringir o acesso a determinados endpoints. 

### Documentação da API com OpenAPI/Swagger
- Utilizar a documentação automática gerada pelo FastAPI com **OpenAPI/Swagger** para documentar os endpoints da API.
- A documentação deve incluir descrições detalhadas dos endpoints, parâmetros, e modelos de resposta.

### TECNOLOGIAS :bulb:

1. [Python]
2. [FastAPI]
3. [PostgreSQL]
4. [SQLAlchemy]
5. [Pytest]
6. [Tokens JWT]
7. [Docker]


## Endpoints da API 

###### GET "/books" -- GET BOOK LIST
- Forneçe uma lista das livros na StandLivros.
- Possui parâmetros de consulta para filtrar através do título, autor, categoria.

###### POST "/books" -- CREATE BOOK
- Permite que novos livros sejam adicionados na StandLivros.

###### PUT "/books/{booking_id}" -- UPDATE BOOK
- Permite que alguma informação sobre o título, autor, categoria e preço do livro podem ser alteradas.

###### DELETE "/books/{booking_id}" -- DELETE BOOK
- Permite excluir um livro da StandLivros.

#### OpenAPI/Swagger
- Após rodar a aplicação no VS Code a documentação e testes podem ser feitos no link:
  
[http://localhost:8000/docs]

#### POSTMAN COLLECTION
- Segue link disponível para testes da API através do Postman

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com)


##### Inicialização do ambiente virtual e download das dependências do projeto

- Para clonar um repositório do GitHub, use o comando git clone seguido da URL do repositório
```sh
git clone https://https://github.com/vitorvogomes/fastapi-stand-livros.git
```

##### Configurar as variáveis de ambiente para acessar o banco de dados PostgreSQL
- Arquivo .env
```sh
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=seu_banco
DATABASE_URL=postgresql://seu_usuario:sua_senha@db:5432/seu_banco
```

- Setar variáveis de ambiente
```sh
source .env
```

#### Configurar o ambiente virtual do python
- Criar ambiente virtual
```sh
python -m venv nomevenv
```

- Inicializar o ambiente virtual
```sh
source nomevenv/bin/activate
```

- Atualizar ferramentas pip
```sh
pip install --upgrade pip
```

- Download das dependencias do projeto
```sh
pip install -r requirements.txt
```
  
#### Docker Compose para incializar os Containers

- Build e Up: Para criar os containers
```sh
docker-compose up --build
```

- Logs
```sh
docker-compose logs
```

- Rebuild e Restart nos containers
```sh
docker-compose down
```

- Up: Para inicializar os containers
```sh
docker-compose up
```

#### Para Rodar localmente e Realizar testes com Pytest

- Rodar pytest
- Rodar o testes e mapear a cobertura em uma determinada rota
```sh
pytest --cov=routers --cov-report=term-missing

```



#### Versões utilizadas no projeto

Ubuntu 24.04.1 LTS
Python 3.12.3
Docker 27.3.1
Docker Compose version v2.30.3
PostgreSQL 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)