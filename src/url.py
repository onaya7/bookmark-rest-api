from flask import Blueprint, redirect
from src.database import db, Bookmark



url = Blueprint("url", __name__)


@url.get('/<short_url>')
def redirect_to_url(short_url):
    bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()
    
    if bookmark:
        bookmark.visits = bookmark.visits +  1
        db.session.commit()
        return redirect(bookmark.url)


