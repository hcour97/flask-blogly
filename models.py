"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(30), 
                           nullable=False)
    
    last_name = db.Column(db.String(30), 
                          nullable=False)
    
    img_url = db.Column(db.String(100), 
                        nullable=False)
    

def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)