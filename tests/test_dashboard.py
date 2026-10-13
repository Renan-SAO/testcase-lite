from app.models import TestCase
from app.services import record_execution
from app import db
from app.services import dashboard_metrics

def test_dashboard_counts_executions_correctly(app, valid_case_data):
    with app.app_context():
        case = TestCase(**valid_case_data)
        db.session.add(case)
        db.session.commit()
        record_execution(case, "APROVADO")
        record_execution(case, "REPROVADO")
        record_execution(case, "BLOQUEADO")
        metrics = dashboard_metrics()
        assert metrics == {
            "cases": 1, "executions": 3, "approved": 1, "failed": 1, "blocked": 1
        }

def test_empty_dashboard_metrics(app):
    with app.app_context():
        assert dashboard_metrics() == {
            "cases": 0, "executions": 0, "approved": 0, "failed": 0, "blocked": 0
        }
