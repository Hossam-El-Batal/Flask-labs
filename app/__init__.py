# app/__init__.py

from flask import Flask
from .models import db
from .auth import auth_bp
from .books import books_bp
from .admin import admin_bp
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(admin_bp)
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(books_bp, url_prefix='/books')

    return app
