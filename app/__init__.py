from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from .routes.api.api import api_bp
    from .routes.main.main import main_bp

    with app.app_context():
        app.register_blueprint(api_bp)
        app.register_blueprint(main_bp)

        db.create_all()

    return app
