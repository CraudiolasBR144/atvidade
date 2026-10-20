import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    base_dir = Path(__file__).resolve().parent.parent
    load_dotenv(base_dir / ".env")

    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "desenvolvimento-troque-esta-chave")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(base_dir / "data.sqlite")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Importar os modelos registra as tabelas no SQLAlchemy.
    from app import models  # noqa: F401
    from app.routes import main
    app.register_blueprint(main)

    @app.errorhandler(404)
    def not_found(_error):
        from flask import render_template
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):
        from flask import render_template
        return render_template("500.html"), 500

    return app
