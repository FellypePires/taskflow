import pytest
from fastapi.testclient import TestClient

from app.main import app, reset_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpa_banco():
    reset_db()
    yield
    reset_db()


def test_busca_tarefa_existente():
    client.post("/tasks", json={"title": "Estudar Git"})

    resposta = client.get("/tasks/1")

    assert resposta.status_code == 200
    assert resposta.json()["title"] == "Estudar Git"


def test_busca_tarefa_inexistente_retorna_404():
    resposta = client.get("/tasks/99")

    assert resposta.status_code == 404
