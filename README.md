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

### Documentação da API com OpenAPI/Swagger
- Utilizar a documentação automática gerada pelo FastAPI com **OpenAPI/Swagger** para documentar os endpoints da API.
- A documentação deve incluir descrições detalhadas dos endpoints, parâmetros, e modelos de resposta.

### Autenticação & Autorização
Esses itens não são obrigatórios, mas serão considerados como bônus e podem demonstrar seu nível de experiência e conhecimento avançado:
- Implementar **Autenticação** de usuários utilizando **JWT (JSON Web Tokens)**.
- Implementar a **Autorização** com uso de Dependências (dependencies) ou Middleware para restringir o acesso a determinados endpoints.

### TECNOLOGIAS :bulb:

1. [Python]
2. [FastAPI]
3. [PostgreSQL]
4. [SQLAlchemy]
5. [Pytest]
6. [Docker]


##### Inicialização do ambiente virtual e download das dependências do projeto

- Para clonar um repositório do GitHub, use o comando git clone seguido da URL do repositório
```sh
git clone https://https://github.com/vitorvogomes/fastapi-stand-livros.git
```

#### Configurar o ambiente virtual do python
- Criar ambiente virtual
```sh
python3 -m venv .venv
```

- Inicializar o ambiente virtual
```sh
source .venv/bin/activate
```

- Atualizar ferramentas pip
```sh
pip install --upgrade pip
```

- Download das dependencias do projeto
```sh
pip install -r requirements.txt
```

#### Para Rodar localmente e Realizar testes com Pytest
###### Renomear as variáveis de ambiente para acessar o banco de dados PostgreSQL
- Renomear a variavel DATABASE_URL manualmente no arquivo .env DATABASE_URL como base de exemplo arquivo .env.pytest
```sh
DATABASE_URL=sqlite:///./test.db
```

- Carregar variáveis de ambiente
```sh
source .env
grep DATABASE_URL .env
```

- Rodar pytest
- Rodar o testes e mapear a cobertura em uma determinada rota
```sh
python3 -m pytest --cov=routers --cov-report=term-missing

```

- Alternativas para rodar os testes
```sh
coverage report -m

```

#### Docker Compose para incializar os Containers
###### Configurar as variáveis de ambiente para acessar o banco de dados PostgreSQL
- Modificar DATABASE_URL para 'db' durante no container no arquivo .env para rodar na produção 
```sh
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecret
POSTGRES_DB=mydatabase
DATABASE_URL=postgresql+psycopg2://postgres:mysecret@db:5432/mydatabase
```

- Setar variáveis de ambiente
```sh
source .env
```

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
coverage run -m pytest test/
docker-compose up
```


##### Configurar as variáveis de ambiente para acessar
###### PRODUÇÃO - CONTAINER DOCKER - ARQUIVO (.env)
- Renomear o arquivo para rodar
```sh
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecret
POSTGRES_DB=mydatabase
DATABASE_URL=postgresql+psycopg2://postgres:mysecret@db:5432/mydatabase
```

###### TESTES COM PYTEST - LOCAL - ARQUIVO (.env)
- Renomear o arquivo para rodar
```sh
DATABASE_URL=sqlite:///./test.db
```



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


#### Versões utilizadas no projeto

- Ubuntu 24.04.1 LTS
- Python 3.12.3
- Docker 27.3.1
- Docker Compose version v2.30.3
- PostgreSQL 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)