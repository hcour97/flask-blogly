"""Make sample data for users db."""

from models import User, db
from app import app

# Create Tables
db.drop_all()
db.create_all()

# Empty table if it isn't already
User.query.delete()

# Add data
granny = User(first_name="Granny", 
              last_name="Smith", 
              img_url="https://www.freshpoint.com/wp-content/uploads/commodity-granny-smith.jpg")

scooby = User(first_name="Scooby",
              last_name="Doo",
              img_url="https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Scooby-Doo.png/150px-Scooby-Doo.png")


# add new users to the session
db.session.add(granny)
db.session.add(scooby)

# commit to the session
db.session.commit()