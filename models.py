"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.Text, 
                           nullable=False)
    
    last_name = db.Column(db.Text, 
                          nullable=False)
    
    img_url = db.Column(db.Text, 
                        nullable=False,
                        default=DEFAULT_IMG_URL)
    
    @property
    def full_name(self):
        """Returns full name of user."""

        return f"{self.first_name} {self.last_name}"
    

