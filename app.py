"""Blogly application."""

from curses import flash
from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
# from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post

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
    """Show recent list pof posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts.html", posts=posts)

####### User Route ########

@app.route('/users')
def list_users():
    """Shows list of all users in the database"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """Display form to create a new user."""
    return render_template('add_user_form.html')

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
    return render_template("user_details.html", user=user)

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
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")

#### POST ROUTE ####

@app.route('/users/<int:user_id>/post/new')
def new_post(user_id):
    """Display form to create a new post."""
    user = User.query.get_or_404(user_id)
    return render_template('new_post_form.html', user=user)

@app.route('/users/<int:user_id>/post/new', methods=["POST"])
def new_posts(user_id):
    """Form that uploads new post to database."""
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form["title"],
        content = request.form["content"],
        user=user)
        
    db.session.add(new_post)
    db.session.commit()
    # flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Display a single post."""

    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show form to edit post."""

    post=Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle Submission to update an existing post."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()
    # flash(f"Post '{post.title}' updated successfully.")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_delete(post_id):
    """Handle submission form to delete an existing post."""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    # flash(f"Post {post.title} deleted.")

    return redirect(f"/users/{post.user_id}")