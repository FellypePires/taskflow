import pytest
from fastapi.testclient import TestClient

from app.main import app, reset_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpa_banco():
    reset_db()
    yield
    reset_db()


def test_sem_filtro_lista_todas_as_tarefas():
    client.post("/tasks", json={"title": "Concluída", "done": True})
    client.post("/tasks", json={"title": "Pendente", "done": False})

    resposta = client.get("/tasks")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_filtra_tarefas_concluidas():
    client.post("/tasks", json={"title": "Concluída", "done": True})
    client.post("/tasks", json={"title": "Pendente", "done": False})

    resposta = client.get("/tasks?done=true")

    assert resposta.status_code == 200
    assert [task["title"] for task in resposta.json()] == ["Concluída"]
