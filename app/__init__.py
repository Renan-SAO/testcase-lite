from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if app.config.get("MAX_CONTENT_LENGTH") is None:
        app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
