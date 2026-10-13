from datetime import datetime, timezone
from app import db

VALID_RESULTS = {"APROVADO", "REPROVADO", "BLOQUEADO"}

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=True, default="")
    preconditions = db.Column(db.Text, nullable=True, default="")
    steps = db.Column(db.Text, nullable=False)
    expected_result = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    executions = db.relationship(
        "TestExecution", backref="test_case", cascade="all, delete-orphan",
        order_by="TestExecution.created_at.desc()"
    )

class TestExecution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"), nullable=False)
    result = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text, nullable=True, default="")
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    evidences = db.relationship(
        "ExecutionEvidence", backref="execution", cascade="all, delete-orphan"
    )


class ExecutionEvidence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    execution_id = db.Column(
        db.Integer, db.ForeignKey("test_execution.id"), nullable=False
    )
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
