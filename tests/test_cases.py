from app.models import TestCase, TestExecution, ExecutionEvidence
from app import db

def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Painel de qualidade" in response.data

def test_create_case_success(client, app, valid_case_data):
    response = client.post("/cases/new", data=valid_case_data, follow_redirects=True)
    assert response.status_code == 200
    assert "Login com dados válidos" in response.get_data(as_text=True)
    with app.app_context():
        assert TestCase.query.count() == 1

def test_create_case_requires_title(client, valid_case_data):
    valid_case_data["title"] = " "
    response = client.post("/cases/new", data=valid_case_data)
    assert response.status_code == 400
    assert "Título é obrigatório" in response.get_data(as_text=True)

def test_create_case_requires_steps(client, valid_case_data):
    valid_case_data["steps"] = ""
    response = client.post("/cases/new", data=valid_case_data)
    assert response.status_code == 400

def test_edit_case(client, app, valid_case_data):
    client.post("/cases/new", data=valid_case_data)
    with app.app_context():
        case_id = TestCase.query.first().id
    valid_case_data["title"] = "Login atualizado"
    response = client.post(f"/cases/{case_id}/edit", data=valid_case_data, follow_redirects=True)
    assert response.status_code == 200
    assert "Login atualizado" in response.get_data(as_text=True)

def test_delete_case(client, app, valid_case_data):
    client.post("/cases/new", data=valid_case_data)
    with app.app_context():
        case_id = TestCase.query.first().id
    response = client.post(f"/cases/{case_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert TestCase.query.count() == 0

def test_unknown_case_returns_404(client):
    assert client.get("/cases/999").status_code == 404


def test_delete_case_also_deletes_execution_history(client, app, valid_case_data):
    client.post("/cases/new", data=valid_case_data)
    with app.app_context():
        case_id = TestCase.query.first().id
    client.post(f"/cases/{case_id}/executions", data={"result": "APROVADO", "notes": "ok"})
    response = client.post(f"/cases/{case_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert TestCase.query.count() == 0
        assert TestExecution.query.count() == 0
