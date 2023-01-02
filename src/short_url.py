from flask import Blueprint, redirect
from flasgger import swag_from
from src.database import Bookmark, db

short_url = Blueprint("short_url", __name__ , url_prefix="/api/v1/")


# Route to handle short_url 
@short_url.get('/<short_url>')
@swag_from('./docs/short_url.yaml')
def redirect_to_url(short_url):
    bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()
    
    if bookmark:
        bookmark.visits = bookmark.visits +  1
        db.session.commit()
        return redirect(bookmark.url)