from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import *
from src.database import Bookmark, db
from flask_jwt_extended import jwt_required, get_jwt_identity
import validators

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.post('/')
@jwt_required()
def add_bookmark():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        # assigning variables to store data from json
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')
        print(body)
        print(url)

        # To check if url is valid
        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            }),     HTTP_400_BAD_REQUEST

        # To check db if url already exist    
        existing_url = Bookmark.query.filter_by(url=url).first()
        if existing_url:
            return jsonify({
                'error':"URL already exists"
            }), HTTP_409_CONFLICT

        # adding checked data into the database 
        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit':bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), HTTP_201_CREATED

@bookmarks.get('/')
@jwt_required()
def get_bookmark():
    # get current user from jwt
    current_user = get_jwt_identity()

    # filter db with the current user
    bookmarks = Bookmark.query.filter_by(user_id= current_user)

    data = []

    for bookmark in bookmarks:
        data.append(
            {
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit':bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
            }
        )
    return jsonify({
        'data':data
    }), HTTP_200_OK