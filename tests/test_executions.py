import pytest
from io import BytesIO
from pathlib import Path
from app.models import ExecutionEvidence
from app.models import TestCase, TestExecution
from app.services import record_execution
from app import db

def _create_case(client, data):
    client.post("/cases/new", data=data)
    with client.application.app_context():
        return TestCase.query.first().id

def test_record_valid_execution(client, app, valid_case_data):
    case_id = _create_case(client, valid_case_data)
    response = client.post(f"/cases/{case_id}/executions", data={"result": "APROVADO", "notes": "Fluxo validado"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Execução registrada" in response.get_data(as_text=True)
    with app.app_context():
        assert TestExecution.query.count() == 1

def test_invalid_execution_result_rejected(app, valid_case_data):
    with app.app_context():
        case = TestCase(**valid_case_data)
        db.session.add(case)
        db.session.commit()
        with pytest.raises(ValueError, match="Resultado inválido"):
            record_execution(case, "TALVEZ")

def test_execution_history_preserved(client, app, valid_case_data):
    case_id = _create_case(client, valid_case_data)
    for result in ("APROVADO", "REPROVADO"):
        client.post(f"/cases/{case_id}/executions", data={"result": result})
    with app.app_context():
        assert TestExecution.query.count() == 2

def test_execution_for_unknown_case_returns_404(client):
    assert client.post("/cases/999/executions", data={"result": "APROVADO"}).status_code == 404


def test_execution_accepts_image_evidence(client, app, valid_case_data):
    case_id = _create_case(client, valid_case_data)
    response = client.post(
        f"/cases/{case_id}/executions",
        data={
            "result": "REPROVADO",
            "notes": "Botão não responde",
            "evidence": (BytesIO(b"\x89PNG\r\n\x1a\n" + b"test content"), "falha.png"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Execução registrada" in response.get_data(as_text=True)
    with app.app_context():
        evidence = ExecutionEvidence.query.one()
        assert evidence.original_filename == "falha.png"
        assert Path(app.instance_path, "evidence", evidence.filename).exists()
        assert client.get(f"/evidence/{evidence.id}").status_code == 200


def test_execution_rejects_non_image_extension(client, app, valid_case_data):
    case_id = _create_case(client, valid_case_data)
    response = client.post(
        f"/cases/{case_id}/executions",
        data={
            "result": "APROVADO",
            "evidence": (BytesIO(b"not an image"), "script.exe"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert "Formato não permitido" in response.get_data(as_text=True)
    with app.app_context():
        assert TestExecution.query.count() == 0


def test_delete_case_removes_uploaded_evidence(client, app, valid_case_data):
    case_id = _create_case(client, valid_case_data)
    client.post(
        f"/cases/{case_id}/executions",
        data={
            "result": "REPROVADO",
            "evidence": (BytesIO(b"\x89PNG\r\n\x1a\n" + b"test content"), "falha.png"),
        },
        content_type="multipart/form-data",
    )
    with app.app_context():
        evidence = ExecutionEvidence.query.one()
        saved_path = Path(app.instance_path, "evidence", evidence.filename)
        assert saved_path.exists()
    client.post(f"/cases/{case_id}/delete")
    assert not saved_path.exists()
    with app.app_context():
        assert ExecutionEvidence.query.count() == 0
