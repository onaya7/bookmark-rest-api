import os
from flask import Flask, jsonify, redirect
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db, Bookmark
from src.constants.http_status_codes import *
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS"),
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY"),

            SWAGGER ={
                'title':"Bookmark API",
                'uiversion':3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    # configure JWTManager
    JWTManager(app)

    #configure Swagger
    Swagger(app, template=template, config=swagger_config)

    #configure Cors
    CORS(app)

    # Registering blueprints
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
   
    # Route to handle short_url 
    @app.get('/<short_url>')
    @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()
        
        if bookmark:
            bookmark.visits = bookmark.visits +  1
            db.session.commit()
            return redirect(bookmark.url)

    # Routes to handle error exceptions
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            'error':"Not found",
        }), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            'error':"Something went wrong, we are working on it"
        }), HTTP_500_INTERNAL_SERVER_ERROR

    return app 