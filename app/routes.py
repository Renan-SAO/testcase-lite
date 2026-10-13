from pathlib import Path
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app import db
from app.models import TestCase, ExecutionEvidence
from app.services import create_case, validate_case, record_execution, dashboard_metrics

bp = Blueprint("main", __name__)

ALLOWED_EVIDENCE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_EVIDENCE_SIZE = 5 * 1024 * 1024


def _looks_like_image(upload, extension):
    upload.stream.seek(0)
    header = upload.stream.read(12)
    upload.stream.seek(0)
    if extension == "png":
        return header.startswith(b"\x89PNG\r\n\x1a\n")
    if extension in {"jpg", "jpeg"}:
        return header.startswith(b"\xff\xd8\xff")
    if extension == "gif":
        return header.startswith((b"GIF87a", b"GIF89a"))
    if extension == "webp":
        return header.startswith(b"RIFF") and header[8:12] == b"WEBP"
    return False


def _evidence_folder():
    folder = Path(current_app.instance_path) / "evidence"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _remove_case_evidence(case):
    for execution in case.executions:
        for evidence in execution.evidences:
            try:
                (_evidence_folder() / evidence.filename).unlink(missing_ok=True)
            except OSError:
                current_app.logger.exception("Não foi possível remover uma evidência.")

@bp.get("/")
def index():
    cases = TestCase.query.order_by(TestCase.created_at.desc()).all()
    return render_template("index.html", cases=cases, metrics=dashboard_metrics())

@bp.route("/cases/new", methods=["GET", "POST"])
def new_case():
    if request.method == "POST":
        case, errors = create_case(request.form)
        if errors:
            for message in errors.values():
                flash(message, "error")
            return render_template("case_form.html", case=None, form=request.form), 400
        flash("Caso de teste cadastrado com sucesso.", "success")
        return redirect(url_for("main.case_detail", case_id=case.id))
    return render_template("case_form.html", case=None, form={})

@bp.route("/cases/<int:case_id>/edit", methods=["GET", "POST"])
def edit_case(case_id):
    case = db.session.get(TestCase, case_id)
    if case is None:
        abort(404)
    if request.method == "POST":
        errors = validate_case(request.form)
        if errors:
            for message in errors.values():
                flash(message, "error")
            return render_template("case_form.html", case=case, form=request.form), 400
        for field in ("title", "description", "preconditions", "steps", "expected_result"):
            setattr(case, field, (request.form.get(field) or "").strip())
        db.session.commit()
        flash("Caso atualizado.", "success")
        return redirect(url_for("main.case_detail", case_id=case.id))
    return render_template("case_form.html", case=case, form={
        field: getattr(case, field) or "" for field in
        ("title", "description", "preconditions", "steps", "expected_result")
    })

@bp.post("/cases/<int:case_id>/delete")
def delete_case(case_id):
    case = db.session.get(TestCase, case_id)
    if case is None:
        abort(404)
    _remove_case_evidence(case)
    db.session.delete(case)
    db.session.commit()
    flash("Caso excluído.", "success")
    return redirect(url_for("main.index"))

@bp.get("/cases/<int:case_id>")
def case_detail(case_id):
    case = db.session.get(TestCase, case_id)
    if case is None:
        abort(404)
    return render_template("case_detail.html", case=case)

@bp.post("/cases/<int:case_id>/executions")
def add_execution(case_id):
    case = db.session.get(TestCase, case_id)
    if case is None:
        abort(404)
    result = request.form.get("result", "")
    upload = request.files.get("evidence")
    stored_path = None
    original_name = ""
    if upload and upload.filename:
        original_name = secure_filename(upload.filename)
        extension = original_name.rsplit(".", 1)[-1].lower() if "." in original_name else ""
        if extension not in ALLOWED_EVIDENCE_EXTENSIONS:
            flash("Formato não permitido. Envie PNG, JPG, JPEG, GIF ou WEBP.", "error")
            return redirect(url_for("main.case_detail", case_id=case.id))
        upload.stream.seek(0, 2)
        size = upload.stream.tell()
        upload.stream.seek(0)
        if size > MAX_EVIDENCE_SIZE:
            flash("A imagem deve ter no máximo 5 MB.", "error")
            return redirect(url_for("main.case_detail", case_id=case.id))
        if not _looks_like_image(upload, extension):
            flash("O arquivo não parece ser uma imagem válida do formato selecionado.", "error")
            return redirect(url_for("main.case_detail", case_id=case.id))
    try:
        execution = record_execution(case, result, request.form.get("notes", ""))
        if upload and upload.filename:
            filename = f"{uuid4().hex}.{extension}"
            stored_path = _evidence_folder() / filename
            upload.save(stored_path)
            evidence = ExecutionEvidence(
                execution_id=execution.id,
                filename=filename,
                original_filename=original_name,
            )
            db.session.add(evidence)
            db.session.commit()
    except ValueError as exc:
        if stored_path and stored_path.exists():
            stored_path.unlink(missing_ok=True)
        flash(str(exc), "error")
        return redirect(url_for("main.case_detail", case_id=case.id))
    flash("Execução registrada.", "success")
    return redirect(url_for("main.case_detail", case_id=case.id))


@bp.get("/evidence/<int:evidence_id>")
def view_evidence(evidence_id):
    evidence = db.session.get(ExecutionEvidence, evidence_id)
    if evidence is None:
        abort(404)
    return send_from_directory(
        _evidence_folder(), evidence.filename, as_attachment=False,
        download_name=evidence.original_filename
    )

@bp.route("/ai-suggestions", methods=["GET", "POST"])
def ai_suggestions():
    requirement = ""
    suggestions = []
    if request.method == "POST":
        requirement = (request.form.get("requirement") or "").strip()
        if not requirement:
            flash("Informe um requisito para gerar sugestões.", "error")
        else:
            # Fallback local determinístico: funciona sem chave ou serviço externo.
            # Não é um modelo generativo; serve como sugestão inicial revisável.
            suggestions = [
                {"title": "Validar o fluxo principal", "steps": f"1. Preparar as condições descritas no requisito.\n2. Executar: {requirement}", "expected": "O sistema atende ao comportamento descrito no requisito."},
                {"title": "Validar entrada inválida ou condição negativa", "steps": f"1. Preparar uma entrada inválida relacionada ao requisito.\n2. Executar: {requirement}", "expected": "O sistema rejeita a entrada inválida e apresenta um comportamento controlado."},
                {"title": "Validar campos ou dados obrigatórios", "steps": "1. Omitir um dado obrigatório relacionado ao requisito.\n2. Tentar concluir a operação.", "expected": "A operação é impedida ou orientada conforme as regras do sistema."}
            ]
            flash("Sugestões iniciais geradas localmente. Revise-as antes de utilizar.", "success")
    return render_template("ai_suggestions.html", requirement=requirement, suggestions=suggestions)
