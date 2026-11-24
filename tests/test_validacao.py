from fastapi.testclient import TestClient

from app.main import app, reset_db

client = TestClient(app)


def test_post_titulo_vazio_retorna_422():
    reset_db()

    resposta = client.post("/tasks", json={"title": ""})

    assert resposta.status_code == 422
    reset_db()


def test_delete_tarefa_inexistente_retorna_404():
    reset_db()

    resposta = client.delete("/tasks/999")

    assert resposta.status_code == 404
    reset_db()
