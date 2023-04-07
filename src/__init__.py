import os
from flask import Flask, jsonify
from src.auth import auth
from src.bookmarks import bookmarks
from src.short_url import short_url
from src.database import db
from src.constants.http_status_codes import *
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from src.config.swagger import template, swagger_config
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get(
                "SQLALCHEMY_TRACK_MODIFICATIONS"),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            WTF_CSRF_SECRET_KEY=os.environ.get("WTF_CSRF_SECRET_KEY"),
            SWAGGER={
                'title': "Bookmark API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    # configure JWTManager
    JWTManager(app)

    # configure Swagger
    Swagger(app, template=template, config=swagger_config)

    # configure Cors
    CORS(app)

    # configure Flask-Migrate
    Migrate(app, db)

    # configure CSRF
    app.config['WTF_CSRF_ENABLED'] = False
    CSRFProtect(app)
    
    
    # Registering blueprints
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(short_url)

    # Routes to handle error exceptions

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            'error': "Not found",
        }), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            'error': "Something went wrong, we are working on it"
        }), HTTP_500_INTERNAL_SERVER_ERROR

    return app
