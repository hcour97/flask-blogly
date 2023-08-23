"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
# from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'so secret'

toolbar = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def root():
    """Homepage. Redirects to list of users."""
    return redirect("/users")

####### User Route ########

@app.route('/users')
def list_users():
    """Shows list of all users in the database"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """Display form to create a new user."""
    return render_template('form.html')

@app.route('/users/new', methods=["POST"])
def users_new():
    """Form that allows a user to be entered into the database."""
    new_user = User(
        first_name = request.form["first_name"],
        last_name = request.form["last_name"],
        img_url = request.form["img_url"] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Shows info about a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user."""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle the form submission when user is updated."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    """Handle submission form to delete an existing user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")