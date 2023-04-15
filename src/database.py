from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
import string
from random import choices

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship('Bookmark', backref='user')
    
    def create_password_hash(self, password):
        self.password = generate_password_hash(password)
        
    def __repr__(self):
        return f"User('id:{self.id}')"

class Bookmark(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        body = db.Column(db.Text(), nullable=True) 
        url = db.Column(db.Text(), nullable=False)
        short_url = db.Column(db.String(3), nullable=False)
        visits = db.Column(db.Integer, default=0)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        created_at = db.Column(db.DateTime, default=datetime.now())
        updated_at = db.Column(db.DateTime, onupdate=datetime.now())

        def generate_short_link(self):
            characters = string.digits + string.ascii_letters
            picked_chars = ''.join(choices(characters, k=3))
            link = self.query.filter_by(short_url=picked_chars).first()

            if link:
                return self.generate_short_link()
            return picked_chars

        def __init__(self, **kwargs):
             super().__init__(**kwargs)
             self.short_url=self.generate_short_link()


        def __repr__(self):
            return f"Bookmarks('id:{self.id}','body:{self.body}' , 'url:{self.url}' )"