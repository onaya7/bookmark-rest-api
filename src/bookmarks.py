from flask import Blueprint, request, jsonify, redirect
from src.constants.http_status_codes import *
from src.database import Bookmark, db
from flask_jwt_extended import jwt_required, get_jwt_identity
import validators
from flasgger import swag_from

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.post('/')
@jwt_required()
@swag_from("./docs/bookmark/add_bookmark.yaml")
def add_bookmark():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        # assigning variables to store data from json
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')
        

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
@swag_from("./docs/bookmark/bookmark.yaml")
def get_bookmark():
    # get current user from jwt
    current_user = get_jwt_identity()

    #working with pagination 
    #setting default page to 1 and asigning 5 pages per page
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # filter db with the current user and adding pagination to filter pages
    bookmarks = Bookmark.query.filter_by(user_id= current_user).paginate(page=page, per_page=per_page)
  

    # creating an empty list to store data 
    #and appending retrieved data to the list  to be sent back as json to the api 
    data = []
    for bookmark in bookmarks.items:
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
    meta= {
        "page": bookmarks.page,
        "pages": bookmarks.pages,
        "total_count": bookmarks.total,
        "prev_page": bookmarks.prev_num,
        "next_page": bookmarks.next_num,
        "has_next": bookmarks.has_next,
        "has_prev": bookmarks.has_prev,
    }
    return jsonify({
        'data':data,
        'meta':meta
    }), HTTP_200_OK



@bookmarks.get('/<int:id>')
@jwt_required()
@swag_from("./docs/bookmark/singlebookmark.yaml")
def get_singlebookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    # if bookmark does not exist send error message
    if not bookmark:
        return jsonify({
            'error':'Item not found'
        }), HTTP_404_NOT_FOUND

    return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit':bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), HTTP_200_OK

@bookmarks.put('/<int:id>')
@jwt_required()
@swag_from("./docs/bookmark/updatebookmark.yaml")
def update_bookmark(id):
    current_user=get_jwt_identity()
    body = request.get_json().get('body')
    url = request.get_json().get('url')

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    # To check if url is valid
    if not validators.url(url):
        return jsonify({
            'error': 'Enter a valid url'
        }),     HTTP_400_BAD_REQUEST

    if not bookmark:
        return jsonify({
            'error':'Item not found'
        }), HTTP_404_NOT_FOUND
   
    else:
        bookmark.body = body
        bookmark.url = url
        db.session.commit()

    return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit':bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), HTTP_200_OK

@bookmarks.delete('/<int:id>')
@jwt_required()
@swag_from("./docs/bookmark/deletebookmark.yaml")
def delete_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    # if bookmark does not exist send error message
    if not bookmark:
        return jsonify({
            'error':'Item not found'
        }), HTTP_404_NOT_FOUND

    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({
           "message":"Item has been deleted successfully"
        }), HTTP_200_OK

@bookmarks.get('/stats')
@jwt_required()
@swag_from("./docs/bookmark/stats.yaml")
def get_stat():
    current_user = get_jwt_identity()

    data =[]

    items = Bookmark.query.filter_by(user_id=current_user).all()

    for item in items:
        new_link ={
            'visits':item.visits,
            'url':item.url,
            'id':item.id,
            'short_url': item.short_url,
        }

        data.append(new_link)

    return jsonify({
        'data':data
    }), HTTP_200_OK
        