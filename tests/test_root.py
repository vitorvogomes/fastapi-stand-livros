import logging
from fastapi.testclient import TestClient
from main import app

logging.basicConfig(level=logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

client = TestClient(app)

# Teste estrutura da resposta e da mensagem em caso de sucesso
def test_get_books(test_many_db):
    response = client.get("/")
    logger.debug(f"Resposta da API: {response.json()}")

    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to StandLivros"
    logger.info("Teste concluído com sucesso: Estrutura de resposta correta.")