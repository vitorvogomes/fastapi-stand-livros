import logging
from fastapi.testclient import TestClient
from unittest.mock import patch
from tests.test_fixtures import test_many_db
from main import app
from services.book_service import Book_List

logging.basicConfig(level=logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

client = TestClient(app)

# Teste estrutura da resposta e da mensagem em caso de sucesso
def test_get_books_success_message(test_many_db):
    response = client.get("/books")
    logger.debug(f"Resposta da API: {response.json()}")

    assert response.status_code == 200
    assert "success" in response.json()
    assert response.json()["success"] == "Livros disponiveis na StandLivros"
    logger.info("Teste concluído com sucesso: Estrutura de resposta correta.")

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




