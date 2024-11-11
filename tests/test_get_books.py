import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from routers.book_routers import book_router  # Importar seu roteador
from routers.book_routers import book_list_service
from main import app  # Substituir por onde você conecta o roteador principal

# Registre seu roteador para teste
app.include_router(book_router)
client = TestClient(app)

def test_get_books_mocked(mocker):
    mock_data = [
        {"id": "1", "titulo": "Livro 1", "autor": "Autor 1", "categoria": "Categoria 1", "valor": 99.99},
        {"id": "2", "titulo": "Livro 2", "autor": "Autor 2", "categoria": "Categoria 2", "valor": 99.99},
        {"id": "3", "titulo": "Livro 3", "autor": "Autor 3", "categoria": "Categoria 3", "valor": 99.99},
    ]

    # Cria mock para a função book_list_service.get
    mocker.patch("book_list_service.get", return_value=mock_data)

    # Faz chamada para a rota com o FastAPI test client
    response = client.get("/books")

    # Verifica se a resposta está como esperado
    assert response.status_code == 200
    assert response.json() == {
        "success": "Livros disponiveis na StandLivros",
        "data": mock_data
    }


"""
# Teste para uso de filtros - Titulo
def test_get_books_by_title(test_many_db):
    response = client.get("/books", params={"titulo": "Livro 1"})
    logger.debug(f"Resposta da API: {response.json()}")

    assert response.status_code == 200
    book = response.json()["data"]
    assert book[0]["titulo"] == "Livro 1"
    logger.info("Teste concluído com sucesso: Filtro de título aplicado corretamente.")

# Teste para uso de filtros - Autor
def test_get_books_by_author(test_many_db):
    response = client.get("/books", params={"autor": "Autor 1"})
    logger.debug(f"Resposta da API: {response.json()}")

    assert response.status_code == 200
    book = response.json()["data"]
    assert book[0]["autor"] == "Autor 1"
    logger.info("Teste concluído com sucesso: Filtro de autor aplicado corretamente.")

# Teste para uso de filtros - Categoria
def test_get_books_by_category(test_many_db):
    response = client.get("/books", params={"categoria": "Categoria 1"})
    logger.debug(f"Resposta da API: {response.json()}")

    assert response.status_code == 200
    book = response.json()["data"]
    assert book[0]["categoria"] == "Categoria 1"
    logger.info("Teste concluído com sucesso: Filtro de categoria aplicado corretamente.")

# Teste para uso de filtros - Todos os filtros
def test_get_books_all_filters(test_many_db):
    response = client.get("/books", params={"titulo": "Livro 1", "autor": "Autor 1", "categoria": "Categoria 1"})
    logger.debug(f"Resposta da API: {response.json()}")

    assert response.status_code == 200
    book = response.json()["data"]
    assert book[0]["categoria"] == "Categoria 1"
    assert book[0]["autor"] == "Autor 1"
    assert book[0]["titulo"] == "Livro 1"
    logger.info("Teste concluído com sucesso: Todos os filtros aplicados corretamente.")

# Teste para ValueError, filtro não encontrado
def test_get_books_not_found(test_many_db):
    with patch.object(Book_List, "get", side_effect=ValueError("Erro inesperado")):
        response = client.get("/books", params={"titulo": "Inexistente"})
        logger.debug(f"Resposta da API: {response.json()}")

        assert response.status_code == 404
        assert "Não localizado:" in response.json()["detail"]
        logger.info("Teste concluído com sucesso: Erro de valor não encontrado acionado.")

# Teste mensagem de erro para exceções
def test_get_books_exception(test_many_db):
    with patch.object(Book_List, "get", side_effect=Exception("Erro inesperado")):
        response = client.get("/books")
        logger.debug(f"Resposta da API: {response.json()}")

        assert response.status_code == 500
        assert "Erro ao listar livros:" in response.json()["detail"]
        logger.info("Teste concluído com sucesso: Erro de exceção acionado.")



"""
