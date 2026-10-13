import pytest
from app import create_app, db

@pytest.fixture()
def app(tmp_path):
    database = tmp_path / "test.db"
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database}",
        "WTF_CSRF_ENABLED": False,
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def valid_case_data():
    return {
        "title": "Login com dados válidos",
        "description": "Validar login feliz",
        "preconditions": "Usuário cadastrado",
        "steps": "1. Abrir login\n2. Informar credenciais",
        "expected_result": "Usuário acessa o sistema",
    }
