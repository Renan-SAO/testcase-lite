from app.models import TestCase, TestExecution, VALID_RESULTS
from app import db

def validate_case(data):
    errors = {}
    for field, label in [
        ("title", "Título"), ("steps", "Passos de execução"),
        ("expected_result", "Resultado esperado")
    ]:
        if not (data.get(field) or "").strip():
            errors[field] = f"{label} é obrigatório."
    if len((data.get("title") or "").strip()) > 160:
        errors["title"] = "O título deve ter no máximo 160 caracteres."
    return errors

def create_case(data):
    errors = validate_case(data)
    if errors:
        return None, errors
    case = TestCase(
        title=data["title"].strip(),
        description=(data.get("description") or "").strip(),
        preconditions=(data.get("preconditions") or "").strip(),
        steps=data["steps"].strip(),
        expected_result=data["expected_result"].strip(),
    )
    db.session.add(case)
    db.session.commit()
    return case, {}

def record_execution(case, result, notes=""):
    if result not in VALID_RESULTS:
        raise ValueError("Resultado inválido.")
    execution = TestExecution(test_case=case, result=result, notes=(notes or "").strip())
    db.session.add(execution)
    db.session.commit()
    return execution

def dashboard_metrics():
    executions = TestExecution.query.all()
    return {
        "cases": TestCase.query.count(),
        "executions": len(executions),
        "approved": sum(e.result == "APROVADO" for e in executions),
        "failed": sum(e.result == "REPROVADO" for e in executions),
        "blocked": sum(e.result == "BLOQUEADO" for e in executions),
    }
