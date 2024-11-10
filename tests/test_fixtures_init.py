import logging
from fastapi.testclient import TestClient
from tests.test_fixtures import test_empty_db, test_one_db, test_many_db
from main import app

logging.basicConfig(level=logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

client = TestClient(app)

def test_get_books_empty(test_empty_db):
    response = client.get("/books")
    logger.debug(f"Resposta da API: {response.json()}")

    assert response.status_code == 200
    books = response.json()["data"]
    assert len(books) == 0
    logger.info("Teste concluído com sucesso: Nenhum livro encontrado.")

def test_get_books_one(test_one_db):
    response = client.get("/books")
    logger.debug(f"Resposta da API: {response.json()}")

    assert response.status_code == 200
    books = response.json()["data"]
    assert len(books) == 1
    logger.info("Teste concluído com sucesso: Um livro encontrado.")

def test_get_books_many(test_many_db):
    response = client.get("/books")
    logger.debug(f"Resposta da API: {response.json()}")

    assert response.status_code == 200
    books = response.json()["data"]
    assert len(books) > 1
    logger.info("Teste concluído com sucesso: Múltiplos livros encontrados.")